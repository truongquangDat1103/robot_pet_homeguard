#pragma once

#include <Arduino.h>

class Microphone {
private:
    uint8_t pin;
    String name;
    static const int bufferSize = 16000;
    int16_t buffer[bufferSize];

public:
    Microphone(uint8_t analogPin, String micName);
    void begin();
    int readMic();
    void record(int seconds);
    void printBuffer(int samplesToPrint);
    void displayInfo();
    int16_t* getBuffer();

    String getName();
} ;

