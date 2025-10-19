#pragma once

#include <Arduino.h>
#include "Audio.h"  // Thư viện ESP32 Audio

class Speaker {
private:
    int bclkPin, lrcPin, dinPin;
    Audio audio;
    String name;

public:
    Speaker(int bclk, int lrc, int din, String spkName );
    void begin();
    void playURL(const char* url);
    void loop();
    void setVolume(int volume);
    void playVolume(int volume, const char* url);
    void run();
    String getName();
    void displayInfo();
};


