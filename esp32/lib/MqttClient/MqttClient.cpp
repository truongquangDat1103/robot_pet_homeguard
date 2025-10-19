#include "MqttClient.h"

MqttClient::MqttClient(const char* host, uint16_t port, const char* clientId,
                       const char* user, const char* pass)
    : client(wifiClient), host(host), port(port), clientId(clientId) {
    if (user) this->user = user;
    if (pass) this->pass = pass;
}

void MqttClient::begin() {
    client.setServer(host.c_str(), port);
}

bool MqttClient::ensureConnected() {
    if (client.connected()) return true;
    // Try to connect
    if (user.length() > 0) {
        if (client.connect(clientId.c_str(), user.c_str(), pass.c_str())) {
            return true;
        }
    } else {
        if (client.connect(clientId.c_str())) {
            return true;
        }
    }
    return false;
}

void MqttClient::loop() {
    client.loop();
}

bool MqttClient::publishJson(const String& topic, const String& json) {
    return client.publish(topic.c_str(), json.c_str());
}

