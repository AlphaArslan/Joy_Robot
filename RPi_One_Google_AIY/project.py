#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys
import time

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
import RPi.GPIO as GPIO
import serial
from gpiozero import PWMOutputDevice



RED = 26
GREEN = 6
BLUE = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)



motor1 = PWMOutputDevice(4)
motor2 = PWMOutputDevice(17)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def motor_on_full():
    aiy.audio.say('Motor On. Full Speed')
    motor1.value = 0.4
    motor2.value = 0.4
    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.HIGH)
    GPIO.output(BLUE,GPIO.LOW)

def motor_off():
    aiy.audio.say('stop')
    motor1.value = 0
    motor2.value = 0
    GPIO.output(RED,GPIO.HIGH)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(BLUE,GPIO.LOW)


def motor_on_right():
    aiy.audio.say('Motor On. Right')
    motor1.value = 0
    motor2.value = 0.3
    GPIO.output(13,GPIO.LOW)
    GPIO.output(26,GPIO.HIGH)
    GPIO.output(6,GPIO.LOW)

def motor_on_left():
    aiy.audio.say('Motor On. Left')
    motor1.value = 0.3
    motor2.value = 0
    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.HIGH)
    GPIO.output(BLUE,GPIO.LOW)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)

    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(BLUE,GPIO.HIGH)

def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)

    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(BLUE,GPIO.HIGH)

def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))

    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(BLUE,GPIO.HIGH)

def process_event(assistant, event):
    print(event)
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()

            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()

            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.HIGH)

        elif text == 'motor on':
            assistant.stop_conversation()
            motor_on_full()

            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'stop':
            assistant.stop_conversation()
            motor_off()

            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'right':
            assistant.stop_conversation()
            motor_on_right()

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'lift':
            assistant.stop_conversation()
            motor_on_left()

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'How many departments in the college ':
            assistant.stop_conversation()
            aiy.audio.say('there are three departments here , electronics , Computer Technology and Communication')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'what is your name':
            assistant.stop_conversation()
            aiy.audio.say('I am the first saudi robot made by Artificial Intelligence , you can call me SARO')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'who is the dean of the college':
            assistant.stop_conversation()
            aiy.audio.say('hi there , how are you , Iam here to help you , what do you want me to do ')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'Tell me about Computer Department':
            assistant.stop_conversation()
            aiy.audio.say('It is one of the most important departments on the saudi colleges level, computer networks technology; management of networks systems technical support and multimedia ')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'what is the best department in the college':
            assistant.stop_conversation()
            aiy.audio.say('i cant really tell , all the department here are amazing , but i am greatful to my inventers i must say ')

            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'hi':
            assistant.stop_conversation()
            aiy.audio.say('hi there , how are you , Iam here to help you , what do you want me to do ')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)



        elif text == 'Tell me about Electronics Technology Department':
            assistant.stop_conversation()
            aiy.audio.say('The electronic technicians here are equiped with all up-to-date scientific information in their fields form both scientific & practical aspects. and they are qualify to work in field of operation and maintenance of industrial facilities')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'Tell me about communications Technology Department':
            assistant.stop_conversation()
            aiy.audio.say('Trainees in this department are brilliants in telecommunications and networks technology. they focuses on , antennas, networks, microwave technologies, satellites, phone systems, and mobile communications')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'How old are you':
            assistant.stop_conversation()
            aiy.audio.say('l am still young , I am younger than your wrinkles show you are , ha ha')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'college info':
            assistant.stop_conversation()
            aiy.audio.say('We have 12 buildings in the college , with variety of technological majors ')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'tell me a joke':
            assistant.stop_conversation()
            aiy.audio.say(' ok , What do computers eat for a snack? ..... microchips!')
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'what is your job':
            assistant.stop_conversation()
            aiy.audio.say('i am here to assisst you and answering all students questions ')
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'who made you':
            assistant.stop_conversation()
            aiy.audio.say('i am a project of 12 brilliant technicians trainees ')
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'who invented you':
            assistant.stop_conversation()
            aiy.audio.say('i am a project of 12 brilliant trainees lead by D.jaber')
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'college for':
            assistant.stop_conversation()
            aiy.audio.say('We have a mosque behind the buildings and a building 48 dedicated to public studies , and also contains the offices of engineers for all disciplines ')

            GPIO.output(RED,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)

        elif text == 'emergency':
            motor_on_full()
            time.sleep(4)
            motor_off()
            aiy.audio.say('what is your emergency')
            time.sleep(8)
            aiy.audio.say('call nine one one')

        elif text == 'where is the electronic department':
            aiy.audio.say('building nine')
            aiy.audio.say('second floor')



    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
