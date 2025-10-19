#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

class MqttClient {
public:
    MqttClient(const char* host, uint16_t port, const char* clientId,
               const char* user = nullptr, const char* pass = nullptr);

    void begin();
    void loop();
    bool ensureConnected();

    bool publishJson(const String& topic, const String& json);

private:
    WiFiClient wifiClient;
    PubSubClient client;
    String host;
    uint16_t port;
    String clientId;
    String user;
    String pass;
};

