from servo import Servo
from camera import Camera
from wink_detector import WinkDetector
import time
from collections import deque

if __name__ == "__main__":
    servo = Servo(pin=15)
    camera = Camera()
    wink_detector = WinkDetector()
    
    CONSECUTIVE_WINK_THRESHOLD = 14
    wink_buff = deque(
        [wink_detector.NO_WINK]*CONSECUTIVE_WINK_THRESHOLD,
        maxlen=CONSECUTIVE_WINK_THRESHOLD
    )
    
    servo.turn_right()
    time.sleep(1)
    
    while True:
        frame = camera.get_latest_frame()
        wink = wink_detector.detect_wink(frame)
        
        wink_buff.append(wink)
        
        if all(x == wink_detector.LEFT_WINK for x in wink_buff):
            servo.turn_right()
            
        elif all(x == wink_detector.RIGHT_WINK for x in wink_buff):
            servo.turn_left()
        
    
        