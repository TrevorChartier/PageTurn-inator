import signal
import sys
import threading
import queue
from servo import Servo
from camera import Camera
from wink_detector import WinkDetector
from servo_worker_thread import ServoWorkerThread
from logger import Logger
from visualize import visualize
import time
from collections import deque

class Main:
    def __init__(self):
        self.__servo = Servo(pin=15)
        self.__camera = Camera()
        self.__wink_detector = WinkDetector()
        self.__logger = Logger("logs/log_video.mp4")
        
        self.__CONSECUTIVE_WINK_THRESHOLD = 14
        self.__wink_buff = deque(
            [self.__wink_detector.NO_WINK]*self.__CONSECUTIVE_WINK_THRESHOLD,
            maxlen=self.__CONSECUTIVE_WINK_THRESHOLD
        )
        
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, self.__cleanup)
        
        # Setup a separate thread and request queue to handle servo requests
        self.__servo_request_queue = queue.Queue()
        self.__servo_worker_thread = ServoWorkerThread(self.__servo, self.__servo_request_queue)
        t = threading.Thread(target=self.__servo_worker_thread.run, daemon=True)
        t.start()
        
    def __cleanup(self, signum, frame):
        print()
        self.__logger.close()
        sys.exit(1)
        
    def start(self):
        self.__servo.turn_right()
        time.sleep(1)
        
        RIGHT_REQUEST =  self.__servo_worker_thread.TURN_RIGHT_REQUEST
        LEFT_REQUEST = self.__servo_worker_thread.TURN_LEFT_REQUEST
        last_request = RIGHT_REQUEST # Prevent duplicate requests
        
        while True:
            frame = self.__camera.get_latest_frame()
            wink = self.__wink_detector.detect_wink(frame)
            
            self.__wink_buff.append(wink)
            
            if all(x == self.__wink_detector.LEFT_WINK for x in self.__wink_buff):
                print("Left Wink Detected")
                if last_request != RIGHT_REQUEST:
                    self.__servo_request_queue.put(RIGHT_REQUEST)
                    last_request = RIGHT_REQUEST
                
            elif all(x == self.__wink_detector.RIGHT_WINK for x in self.__wink_buff):
                print("Right Wink Detected")
                if last_request != LEFT_REQUEST:
                    self.__servo_request_queue.put(LEFT_REQUEST)
                    last_request = LEFT_REQUEST
            
            face_landmarks = self.__wink_detector.get_face_landmarks()
            logging_frame = visualize(frame, face_landmarks)
            self.__logger.write(logging_frame)

if __name__ == "__main__":
    main = Main()
    main.start()
    
        