import queue
from servo import Servo

class ServoWorkerThread:
    def __init__(self, servo: Servo, request_queue: queue.Queue):
        self.__servo = servo
        self.TURN_LEFT_REQUEST = 0
        self.TURN_RIGHT_REQUEST = 1
        self.__request_queue = request_queue
        
    def run(self):
        while True:
            request = self.__request_queue.get()
            if request ==  self.TURN_LEFT_REQUEST:
                self.__servo.turn_left()
            elif  request == self.TURN_RIGHT_REQUEST:
                self.__servo.turn_right()
            else:
                print("Warning: Invalid Request to ServoWorkerThread")