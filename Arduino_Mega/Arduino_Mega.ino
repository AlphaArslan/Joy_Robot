/**************************** Include ****************************/
#include <Wire.h>
// #include <Servo.h>
#include "LedControl.h"

/**************************** Define *****************************/
// constants
#define         SLAVE_ADDRESS                 0x04
#define         ONE_FACE_CODE                 1           // from I2C code table
#define         TWO_FACE_CODE                 2           // from I2C code table
#define         MOVE_DELAY                    800         // in milliseconds
#define         DEVICES_NUMBER                4
#define         BRIGHTNESS                    8

// // servo angles
// #define         SALUT_RU_ANGLE                90          // Right upper servo angle for SALUT move
// #define         SALUT_RL_ANGLE                45          // Right Lower servo angle for SALUT move
// #define         SALUT_LU_ANGLE                90          // Left upper servo angle for SALUT move
// #define         SALUT_LL_ANGLE                45          // Left Lower servo angle for SALUT move

// // pin connections
// #define         RIGHT_UPPER_SERVO             4
// #define         RIGHT_LOWER_SERVO             5
// #define         LEFT_UPPER_SERVO              6
// #define         LEFT_LOWER_SERVO              7
// #define         HEAD_HOR_SERVO                8           // horizontal
// #define         HEAD_VER_SERVO                9           // vertical

/************************* Global Var. ***************************/
int number = 0;
// Servo RU_servo;                                           //Right Upper Servo
// Servo RL_servo;                                           //Right Lower Servo
// Servo LU_servo;                                           //Left Upper Servo
// Servo LL_servo;                                           //Left Lower Servo
// Servo HH_servo;                                           //Head horizontal servo
// Servo HV_servo;                                           //Head vertical servo
//
//Pin 12 = DIN, Pin 11 = CLK, Pin 10 = CS
LedControl lc=LedControl(12,11,10,DEVICES_NUMBER);

/************************** Functions ****************************/
void one_face_detected();
void two_faces_detected();
void smily_face_one();
void smily_face_two();
void clear_screen();
void map_rows(int row, byte left, byte right);

/**************************** Setup() ****************************/
void setup() {
    // RU_servo.attach(RIGHT_UPPER_SERVO);
    // RL_servo.attach(RIGHT_LOWER_SERVO);
    // LU_servo.attach(LEFT_UPPER_SERVO);
    // LL_servo.attach(LEFT_LOWER_SERVO);
    // HH_servo.attach(HEAD_HOR_SERVO);
    // HV_servo.attach(HEAD_VER_SERVO);

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
        switch (number) {
          case ONE_FACE_CODE: one_face_detected(); break;
          case TWO_FACE_CODE: two_faces_detected(); break;
        }
    }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

void one_face_detected(){
    // salut using right arm
    // RU_servo.write(SALUT_RU_ANGLE);\
    // RL_servo.write(SALUT_RL_ANGLE);
    smily_face_one();
    delay(MOVE_DELAY);
    // RU_servo.write(0);
    // RL_servo.write(0);
    clear_screen();
}

void two_faces_detected(){
    // salut using two arms
    // RU_servo.write(SALUT_RU_ANGLE);
    // LU_servo.write(SALUT_LU_ANGLE);
    // RL_servo.write(SALUT_RL_ANGLE);
    // LL_servo.write(SALUT_LL_ANGLE);
    smily_face_two();
    delay(MOVE_DELAY);
    // RU_servo.write(0);
    // LU_servo.write(0);
    // RL_servo.write(0);
    // LL_servo.write(0);
    clear_screen();
}

void smily_face_one() {

}

void smily_face_two() {

}

void clear_screen(){

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
        ROW 0   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 1   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 2   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 3   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 4   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 5   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 6   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 7   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        --------|-------------------------------------|-------------------------------------|
        ROW 8   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 9   |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 11  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 10  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 12  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 14  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 13  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        ROW 15  |   *    *   *   *   *   *   *   *    |    *    *   *   *   *   *   *   *   |
        --------|-------------------------------------|-------------------------------------|
    */
}
