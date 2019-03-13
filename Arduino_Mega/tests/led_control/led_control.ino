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
            for (int col = 0; col < 8; col++) {
                lc.setLed(device, row, col, true);
                delay(200);
            }
        }
    }

    delay(2000);

    for (int device = 0; device < DEVICES_NUMBER; device++) {
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                lc.setLed(device, row, col, false);
                delay(200);
            }
        }
    }

}
