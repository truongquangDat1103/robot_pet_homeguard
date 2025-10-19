#pragma once

// MQTT configuration
#define MQTT_HOST "test.mosquitto.org"   // Change to your broker host/IP
#define MQTT_PORT 1883
#define MQTT_USER ""                    // optional
#define MQTT_PASS ""                    // optional
#define MQTT_CLIENT_ID "homeguard-esp32"

// Base topic, e.g., homeguard/<device_id>/sensor
#define MQTT_TOPIC_BASE "homeguard/esp32"

