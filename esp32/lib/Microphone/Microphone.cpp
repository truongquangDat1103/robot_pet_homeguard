#include "Microphone.h"

Microphone::Microphone(uint8_t analogPin, String micName)
: pin(analogPin), name(micName) {}

void Microphone::begin() {
    pinMode(pin, INPUT);
}

int Microphone::readMic() {
    return analogRead(pin);
}

void Microphone::record(int seconds) {
    int sampleRate = 16000;
    int totalSamples = sampleRate * seconds;
    if (totalSamples > bufferSize) totalSamples = bufferSize;

    Serial.println("🎙️ Ghi âm...");
    for (int i = 0; i < totalSamples; i++) {
        int val = readMic();           // 0–4095 (ADC 12-bit)
        buffer[i] = (val - 2048) * 16;   // Chuẩn hóa sang 16-bit signed
        delayMicroseconds(62);           // ~16kHz sample rate
    }
}
void Microphone::printBuffer(int samplesToPrint) {
    Serial.println("📊 Dữ liệu ghi âm:");
    for (int i = 0; i < samplesToPrint; i++) {
        Serial.println(buffer[i]);
        delay(1);  // tránh tràn Serial Monitor
    }
}

int16_t* Microphone::getBuffer() {
    return buffer;
}


String Microphone::getName() {
    return name;
}

void Microphone::displayInfo() {
    Serial.println("Microphone: " + name);
    Serial.println("Analog pin: " + String(pin));
}
