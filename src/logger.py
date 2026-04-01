"""Provides the Logger class for video logging."""

import cv2

class Logger():
    """Handles video logging on a frame by frame basis."""

    def __init__(self, path):
        """Initializes the Logger.

        Args:
            path (str): File path where the output video will be saved.
        """
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.__writer = cv2.VideoWriter(
            path,
            fourcc, 50.0,
            (640, 480)
        )

    def write(self, frame):
        """Writes a frame to the video file.

        Args:
            frame (np.ndarray): The video frame to write.
        """
        self.__writer.write(frame)

    def close(self):
        """Releases the video writer if it is open."""
        print("Closing Logger Resources")
        if self.__writer.isOpened():
            self.__writer.release()