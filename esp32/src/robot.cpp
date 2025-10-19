#include "robot.h"

Robot::Robot()
       : screen(),
         wifi("LE HUE", "012345679", 10000),
         ultrasonicSensor(ULTRASONIC_TRIG_PIN, ULTRASONIC_ECHO_PIN, "Ultrasonic Sensor"),
         gasSensor(GAS_SENSOR_PIN, 500, "Gas Sensor"),
         dhtSensor(DHT_PIN, DHT11, "DHT Sensor"),
         motionSensor(PIR_PIN, 200, "PIR Sensor"),
         flameSensor(FLAME_PIN, 200, "Flame Sensor"),
         speaker(SPK_BCLK_PIN, SPK_LRC_PIN, SPK_DIN_PIN, "MAX98357A"),
         microphone(MIC_PIN, "MAX9814"),
         mqtt(MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USER, MQTT_PASS)
{}

void Robot::begin() {
    Serial.begin(115200);
    screen.begin();
    wifi.connect();
    mqtt.begin();

    ultrasonicSensor.begin();
    gasSensor.begin();
    dhtSensor.begin();
    motionSensor.begin();
    flameSensor.begin();
    speaker.begin();
    microphone.begin();
    Serial.println("Robot initialized.");
}

void Robot::run() {
    screen.playAll();

    mqtt.ensureConnected();
    mqtt.loop();

    flameSensor.isFlameDetected(); // Cập nhật trạng thái lửa
    motionSensor.isMotionDetected(); // Cập nhật trạng thái chuyển động


    float distance = ultrasonicSensor.readDistance();
    int gas = gasSensor.readRaw();
    float temp = dhtSensor.getTemperature();
    float hum = dhtSensor.getHumidity();
    bool motion = motionSensor.getState();
    bool flame = flameSensor.getState();
    Serial.printf("Distance: %.1f cm, Gas: %d, Temp: %.1f C, Hum: %.1f %%, Motion: %s, Flame: %s\n",
                  distance, gas, temp, hum,
                  motion ? "YES" : "NO",
                  flame ? "YES" : "NO");

    String payload;
    payload = String("{\"distance_cm\":") + String(distance, 1) + "}";
    mqtt.publishJson(String(MQTT_TOPIC_BASE) + "/ultrasonic", payload);

    payload = String("{\"gas_raw\":") + String(gas) + "}";
    mqtt.publishJson(String(MQTT_TOPIC_BASE) + "/gas", payload);

    payload = String("{\"temperature_c\":") + String(temp, 1) + ",\"humidity\":" + String(hum, 1) + "}";
    mqtt.publishJson(String(MQTT_TOPIC_BASE) + "/dht", payload);

    payload = String("{\"motion\":") + (motion ? "true" : "false") + "}";
    mqtt.publishJson(String(MQTT_TOPIC_BASE) + "/pir", payload);

    payload = String("{\"flame\":") + (flame ? "true" : "false") + "}";
    mqtt.publishJson(String(MQTT_TOPIC_BASE) + "/flame", payload);

    // delay(500);
}

