#include "Speaker.h"


Speaker::Speaker(int bclk, int lrc, int din, String spkName)
: bclkPin(bclk), lrcPin(lrc), dinPin(din), name(spkName) {}

void Speaker::begin() {
    audio.setPinout(bclkPin, lrcPin, dinPin);
    audio.setVolume(15);
}

void Speaker::playURL(const char* url) {
    audio.connecttohost(url);
}

void Speaker::loop() {
    audio.loop();
}

void Speaker::setVolume(int volume) {
    audio.setVolume(volume);
}

void Speaker::playVolume(int volume, const char* url) {
    setVolume(volume);
    playURL(url);
}


String Speaker::getName() {
    return name;
}
 
void Speaker::displayInfo() {
    Serial.println("Speaker: " + name);
    Serial.printf("BCLK: %d, LRC: %d, DIN: %d\n", bclkPin, lrcPin, dinPin);
}
