/**************************** Include ****************************/
#include <Wire.h>
#include "LedControl.h"

/**************************** Define *****************************/
// constants
#define         SLAVE_ADDRESS                 0x04
#define         ONE_FACE_CODE                 1           // from I2C code table
#define         TWO_FACE_CODE                 2           // from I2C code table
#define         MOVE_DELAY                    800         // in milliseconds
#define         DEVICES_NUMBER                4
#define         BRIGHTNESS                    8

/************************* Global Var. ***************************/
int number = 0;

//Pin 12 = DIN, Pin 11 = CLK, Pin 10 = CS
LedControl lc=LedControl(12,11,10,DEVICES_NUMBER);


byte normal_1[]={
  0b00000000 , 0b00000000 ,
  0b00010000 , 0b00010000 ,
  0b00111000 , 0b00111000 ,
  0b01111100 , 0b01111100 ,
  0b01111100 , 0b01111100 ,
  0b00111000 , 0b00111000 ,
  0b00010000 , 0b00010000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000 ,
  0b00001111 , 0b11110000 ,
  0b00001111 , 0b11110000 ,
  0b00001111 , 0b11110000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000
};

byte normal_2[]={
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00111110 , 0b01111100 ,
    0b00111110 , 0b01111100 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00001111 , 0b11110000 ,
    0b00001111 , 0b11110000 ,
    0b00001111 , 0b11110000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000 ,
    0b00000000 , 0b00000000
};

byte smily[]={
  0b00000000 , 0b00000000 ,
  0b00010000 , 0b00010000 ,
  0b00111000 , 0b00111000 ,
  0b01111100 , 0b01111100 ,
  0b01111100 , 0b01111100 ,
  0b00111000 , 0b00111000 ,
  0b00010000 , 0b00010000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000 ,
  0b00001111 , 0b11110000 ,
  0b00011111 , 0b11111000 ,
  0b00001111 , 0b11110000 ,
  0b00000011 , 0b11000000 ,
  0b00000000 , 0b00000000 ,
  0b00000000 , 0b00000000
};

/************************** Functions ****************************/
void smily_face();
void clear_screen();
void map_rows(int row, byte left, byte right);
byte reverse_byte(byte);

/**************************** Setup() ****************************/
void setup() {

    for (int i = 0; i < DEVICES_NUMBER; i++) {
        lc.shutdown(i, false);
        lc.setIntensity(i, BRIGHTNESS);
        lc.clearDisplay(i);
    }

    Serial.begin(9600); // start serial for output
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");

    for(int i = 0; i<16; i++){
        map_rows(i, normal_2[i*2], normal_2[i*2 +1]);
    }
}

/**************************** loop() *****************************/
void loop() {
    delay(100);
}

/*********************** Func. Definition *************************/
// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
      number = Wire.read();
      Serial.print("data received: ");
      Serial.println(number);
      smily_face();
  }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

void smily_face() {
    clear_screen();
    for(int i = 0; i<16; i++){
        map_rows(i, smily[i*2], smily[i*2 +1]);
    }
    delay(MOVE_DELAY);
    clear_screen();
    for(int i = 0; i<16; i++){
        map_rows(i, normal_2[i*2], normal_2[i*2 +1]);
    }
}

void clear_screen(){
  lc.clearDisplay(0);
  lc.clearDisplay(1);
  lc.clearDisplay(2);
  lc.clearDisplay(3);
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
        lc.setRow(0, 15-row, reverse_byte(left));
        lc.setRow(1, 15-row, reverse_byte(right));
    }else{
        lc.setRow(3, row, left);
        lc.setRow(2, row, right);
    }
}

byte reverse_byte(byte b){
    b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
    b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
    b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
    return b;
}
