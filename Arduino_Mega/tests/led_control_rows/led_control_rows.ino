#include "LedControl.h"

#define       DEVICES_NUMBER          4
#define       BRIGHTNESS              8

//Pin 12 = DIN, Pin 11 = CLK, Pin 10 = CS
LedControl lc=LedControl(12,11,10,DEVICES_NUMBER);

void setup() {
    for (int i = 0; i < DEVICES_NUMBER; i++) {
        lc.shutdown(i, false);
        lc.setIntensity(i, BRIGHTNESS);
        lc.clearDisplay(i);
    }
}

void loop() {
    for (int device = 0; device < DEVICES_NUMBER; device++) {
        for (int row = 0; row < 8; row++) {
            lc.setRow(device, row, 0b00110000);
            delay(80);
            lc.setRow(device, row, 0b00001100);
            delay(80);
            lc.setRow(device, row, 0b00000000);
        }
    }
}
