from smbus2 import SMBus
from adafruit_servokit import ServoKit
import time

################ constants
SALUT_DELAY       = 2                              # in seconds

# servo angles
SALUT_RU_ANGLE    = 90                             # Right upper servo angle for SALUT move
SALUT_RL_ANGLE    = 45                             # Right Lower servo angle for SALUT move
SALUT_LU_ANGLE    = 90                             # Left upper servo angle for SALUT move
SALUT_LL_ANGLE    = 45                             # Left Lower servo angle for SALUT move

# servo channel number
RIGHT_UPPER_SERVO = 1
RIGHT_LOWER_SERVO = 2
LEFT_UPPER_SERVO  = 3
LEFT_LOWER_SERVO  = 4
HEAD_HOR_SERVO    = 5                              # horizontal
HEAD_VER_SERVO    = 6                              # vertical

################ Setup
kit = ServoKit(channels=16)
def move_servos(faces):
    if faces is 1:
        kit.servo[RIGHT_UPPER_SERVO].angle = SALUT_RU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = SALUT_LU_ANGLE
        time.sleep(SALUT_DELAY)
        kit.servo[RIGHT_UPPER_SERVO].angle = 0
        kit.servo[RIGHT_LOWER_SERVO].angle = 0

    elif faces > 1:
        kit.servo[RIGHT_UPPER_SERVO].angle = SALUT_RU_ANGLE
        kit.servo[LEFT_UPPER_SERVO].angle  = SALUT_LU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = SALUT_RL_ANGLE
        kit.servo[LEFT_LOWER_SERVO].angle  = SALUT_LL_ANGLE
        time.sleep(SALUT_DELAY)
        kit.servo[RIGHT_UPPER_SERVO].angle = 0
        kit.servo[LEFT_UPPER_SERVO].angle  = 0
        kit.servo[RIGHT_LOWER_SERVO].angle = 0
        kit.servo[LEFT_LOWER_SERVO].angle  = 0

if __name__ == '__main__':
    while True:
        move_servos(1)
        time.sleep(3)
        move_servos(2)
        time.sleep(3)
