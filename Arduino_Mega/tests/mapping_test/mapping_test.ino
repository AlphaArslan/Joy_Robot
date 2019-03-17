/**************************** Include ****************************/
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
    for (int row = 0; row < 16; row++) {
        map_rows(row, 255, 255);
        delay(1000);
        lc.clearDisplay(0);
        lc.clearDisplay(1);
        lc.clearDisplay(2);
        lc.clearDisplay(3);
    }
}


void map_rows(int row, byte left, byte right){
    // Warning : this function depends directly on how 8x8 matrix are orienred an placed
    // forming the bigger 16x16 matrix
    // this function takes number of row [0-15] and two bytes one for right half
    // and the other one for the left half
    // and considering the placement of 8x8 devices, it maps those values into the
    // coresponding device, row, and byte values
    /*
                |                LEFT HALF            |            RIGHT HALF               |
        --------|-------------------------------------|-------------------------------------|
        ROW 0   |   *    *   *   *   *   *  01  00    |    *    *   *   *   *   *  01  00   |
        ROW 1   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 2   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 3   |   *    *   DEVICE  *   *   *   *    |    *    *   DEVICE  *   *   *   *   |
        ROW 4   |   *    *   * 3 *   *   *   *   *    |    *    *   * 2 *   *   *   *   *   |
        ROW 5   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 6   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 7   |  77   76   *   *   *   *   *   *    |   77   76   *   *   *   *   *   *   |
        --------|-------------------------------------|-------------------------------------|
        ROW 8   |   *    *   *   *   *   *  76  77    |    *    *   *   *   *   *  76  77   |
        ROW 9   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 11  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 10  |   *    *   DEVICE  *   *   *   *    |    *    *   DEVICE  *   *   *   *   |
        ROW 12  |   *    *   * 0 *   *   *   *   *    |    *    *   * 1 *   *   *   *   *   |
        ROW 14  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 13  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 15  |  00   01   *   *   *   *   *   *    |   00   01   *   *   *   *   *   *   |
        --------|-------------------------------------|-------------------------------------|
    */

    if(row > 7){
        lc.setRow(0, 15-row, left);
        lc.setRow(1, 15-row, right);
    }else{
        lc.setRow(3, row, reverse_byte(left));
        lc.setRow(2, row, reverse_byte(right));
    }
}

byte reverse_byte(byte b){
    b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
    b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
    b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
    return b;
}
