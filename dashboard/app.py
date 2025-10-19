import asyncio
import json
from typing import List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from paho.mqtt.client import Client as MqttClient


MQTT_BROKER = "test.mosquitto.org"  # match esp32 include/config.h
MQTT_PORT = 1883
MQTT_TOPIC = "homeguard/esp32/#"

app = FastAPI()
_mqtt_client: Optional[MqttClient] = None


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: str):
        living = []
        for ws in self.active:
            try:
                await ws.send_text(message)
                living.append(ws)
            except Exception:
                # drop broken sockets
                pass
        self.active = living


manager = ConnectionManager()


@app.get("/")
async def root():
    return HTMLResponse(open(__file__.replace("app.py", "index.html"), "r", encoding="utf-8").read())


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                msg = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                try:
                    data = json.loads(msg)
                    # Expect {"type":"cmd", "path":"speaker/volume", "payload":{...}}
                    if isinstance(data, dict) and data.get("type") == "cmd":
                        path = data.get("path", "")
                        payload = data.get("payload", {})
                        publish_cmd(path, payload)
                except Exception:
                    # ignore malformed client messages
                    pass
            except asyncio.TimeoutError:
                # keep loop alive
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def start_mqtt(loop: asyncio.AbstractEventLoop):
    global _mqtt_client
    mqtt = MqttClient()

    def on_connect(client, userdata, flags, rc):
        client.subscribe(MQTT_TOPIC)

    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8", errors="ignore")
        data = f"{{\"topic\":\"{msg.topic}\",\"payload\":{payload}}}"
        # Schedule coroutine on FastAPI's event loop from MQTT thread
        asyncio.run_coroutine_threadsafe(manager.broadcast(data), loop)

    mqtt.on_connect = on_connect
    mqtt.on_message = on_message
    mqtt.connect(MQTT_BROKER, MQTT_PORT, keepalive=30)

    def loop_forever():
        mqtt.loop_forever()

    import threading
    threading.Thread(target=loop_forever, daemon=True).start()
    _mqtt_client = mqtt


@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_running_loop()
    start_mqtt(loop)


def publish_cmd(path: str, payload: dict):
    """Publish a command JSON to MQTT under base/cmd/<path>."""
    global _mqtt_client
    if not _mqtt_client:
        return False
    topic = f"{MQTT_TOPIC.rsplit('/#',1)[0]}/cmd/{path}"
    try:
        _mqtt_client.publish(topic, json.dumps(payload))
        return True
    except Exception:
        return False
