#pragma once

#include <Arduino.h>
#include "Screen.h"
#include "UltrasonicSensor.h"
#include "GasSensor.h"   
#include "DHTSensor.h"
#include <MotionSensor.h>
#include <FlameSensor.h>
#include "Speaker.h"
#include "Microphone.h"
#include "WiFiConnector.h"
#include "config.h"
#include "MqttClient.h"
#include "pins.h"

class Robot {
private:
    Screen screen;          // Quản lý màn hình/video
    WiFiConnector wifi;     // Quản lý kết nối WiFi
    UltrasonicSensor ultrasonicSensor; // Cảm biến siêu âm
    GasSensor gasSensor;         // Cảm biến khí gas MQ-2
    DHTSensor dhtSensor;         // Cảm biến nhiệt độ và độ ẩm DHT11
    MotionSensor motionSensor;   // Cảm biến chuyển động PIR
    FlameSensor flameSensor;     // Cảm biến lửa
    Speaker speaker;             // Loa
    Microphone microphone;       // Mic thu âm
    MqttClient mqtt;             // MQTT client
public:
    Robot();                     // Constructor
    void begin();                // Khởi tạo hệ thống
    void run();                  // Chạy robot
};
