from adafruit_servokit import ServoKit
import time

class Servo:
    """Class for Abstracting the Control of a Physical Servo With PCA9685"""
    def __init__(self, pin=0):
        kit = ServoKit(channels=16)
        self.__servo = kit.servo[pin]
        
    def turn_left(self):
        self.__servo.angle = 1
        
    def turn_right(self):
        self.__servo.angle = 180