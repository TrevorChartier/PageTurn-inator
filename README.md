# The PageTurn-inator
A hands-free, wink-activated robotic page turner for sheet music, built from scratch in under 12 hours.

https://github.com/user-attachments/assets/7b45f7c9-d103-4e64-a657-9321ef7d5e90

## Problem Statement

The idea for this project came about as I was practicing a new piano piece, and I became annoyed with having to stop playing mid-song to turn 
the page. I didn't want  to memorize the piece, so I decided to engineer a completely hands-free way to turn the sheet music while playing.

Once I came up with the idea, I challenged myself to completea full working prototype, including the physical build and software, in under 12-hours. This was a success (barely!), and I later expanded the software to include a visualization and logging pipeline to record the system in action.

## Technical Highlights
To make the system responsive and reliable, I had to solve a few specific engineering challenges:

* **Perception & Wink Detection**: Utilized MediaPipe's Face Landmarker to extract 3D facial landmarks in real-time. I implemented an Eye Aspect Ratio (EAR) algorithm to measure the distance between specific eyelid landmarks. By comparing the EAR of the left and right eyes against a tuned threshold over a consecutive frame buffer, the system accurately filters out natural blinks and only triggers on intentional winks.

* **Multi-threaded Execution (Decoupling Hardware & Software)**: To avoid tearing the page, I used smooth, interpolated servo movements. These take time and block the main execution thread. To prevent the camera feed and perception loop from lagging while the page is turning, I implemented a ServoWorkerThread. The main vision loop pushes directional commands to a thread-safe Queue, allowing the servo to execute its motion asynchronously while the camera continues tracking at a high framerate.


* **Hardware/Software Integration**: Runs on Raspberry Pi 5, interfaces with a Raspberry Pi Camera (via Picamera2), and drives a physical servo motor using the PCA9685 controller.

## Scrappy (literally, made from scraps) Prototype Build
### *Front*
<img src="https://github.com/user-attachments/assets/51f83979-7685-4314-bc6c-e866e0491654" width="300"/>

### *Back*
<img src="https://github.com/user-attachments/assets/01c4900e-68f9-4d4b-8fa2-bc264893ceb8" width="300"/>

## Future Work
Currently, the system is limited to a single bi-directional page turn (supporting up to four-page compositons). In the future, I'd like to explore an electromagnet-based 'picker' system to enable the sequential handling of an arbitrary number of pages.
## Repository Structure

* `main.py`: The core execution loop managing the camera, frame buffer, and threading.

* `wink_detector.py`: The perception module handling MediaPipe inference and EAR math.

* `servo.py` & `servo_worker_thread.py`: Hardware abstraction and queue-based concurrency for smooth motor control.

* `camera.py` & `logger.py`: Video capture and debug logging.

* `visualize.py`: OpenCV utilities for drawing facial meshes and system states.


---
![Untitled drawing](https://github.com/user-attachments/assets/ef2e36fe-8692-4f69-b25b-76cd9479c6d5)

