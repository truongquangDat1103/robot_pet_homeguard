import asyncio
import json
from typing import List, Optional

import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from paho.mqtt.client import Client as MqttClient


MQTT_BROKER = "test.mosquitto.org"  # match esp32 include/config.h
MQTT_PORT = 1883
MQTT_TOPIC = "homeguard/esp32/#"

app = FastAPI()
_mqtt_client: Optional[MqttClient] = None

# Ensure repo root is on sys.path so we can import helpers if needed
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Simple OpenCV-based processors for face detection and motion
try:
    import cv2  # type: ignore
except Exception:
    cv2 = None

ESP32_STREAM_URL = os.environ.get("ESP32_STREAM_URL", "http://172.20.10.2:81/stream")


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


def _mjpeg_response(gen):
    return StreamingResponse(gen, media_type='multipart/x-mixed-replace; boundary=frame')


def _open_capture():
    if cv2 is None:
        raise RuntimeError("OpenCV is not available. Install opencv-python.")
    cap = cv2.VideoCapture(ESP32_STREAM_URL)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open ESP32 stream at {ESP32_STREAM_URL}")
    return cap


def _encode_jpeg(frame):
    ok, buf = cv2.imencode('.jpg', frame)
    if not ok:
        return None
    return buf.tobytes()


def _gen_face_stream():
    cap = None
    try:
        cap = _open_capture()
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') if cv2 else None
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if cascade is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, 'Face', (x, max(0, y-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            data = _encode_jpeg(frame)
            if data is None:
                continue
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + data + b"\r\n")
    finally:
        try:
            if cap is not None:
                cap.release()
        except Exception:
            pass


def _gen_motion_stream():
    cap = None
    try:
        cap = _open_capture()
        fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True) if cv2 else None
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if fgbg is not None:
                fgmask = fgbg.apply(frame)
                blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                motion = False
                for c in contours:
                    if cv2.contourArea(c) < 500:
                        continue
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    motion = True
                if motion:
                    cv2.putText(frame, 'Motion', (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            data = _encode_jpeg(frame)
            if data is None:
                continue
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + data + b"\r\n")
    finally:
        try:
            if cap is not None:
                cap.release()
        except Exception:
            pass


@app.get("/stream/face")
def stream_face():
    return _mjpeg_response(_gen_face_stream())


@app.get("/stream/motion")
def stream_motion():
    return _mjpeg_response(_gen_motion_stream())


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
