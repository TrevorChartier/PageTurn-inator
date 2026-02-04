from adafruit_servokit import ServoKit
import time

class Servo:
    """Class for Abstracting the Control of a Physical Servo With PCA9685"""
    def __init__(self, pin=0):
        kit = ServoKit(channels=16)
        self.__servo = kit.servo[pin]
        
        self.__current_angle = 180
        self.turn_right()
        
    def turn_left(self):
        self.__move_smooth(1, 0.6, 75)
        
    def turn_right(self):
        self.__move_smooth(180, 0.6, 75)
        
    def __move_smooth(self, target_angle, duration=1.0, steps=50):
        start_angle = self.__current_angle
        step_angle = (target_angle - start_angle) / steps
        step_time = duration / steps
        
        for i in range(steps):
            self.__servo.angle = start_angle + (step_angle * i)
            time.sleep(step_time)
            
        self.__current_angle = target_angle