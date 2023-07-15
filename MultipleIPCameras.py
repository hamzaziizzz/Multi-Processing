import multiprocessing
import cv2
from threading import Thread
from multiprocessing import freeze_support

from LiveStreaming import read_frames
from SharedBuffer import SHARED_BUFFER

# Define the camera IP addresses
camera_ips = [
    "192.168.1.6"
]
print("Process 1 Started")


# Define a class to handle camera streaming in a separate thread
class CameraStream(Thread):
    def __init__(self, camera_ip: str):
        Thread.__init__(self)
        self.camera_ip = camera_ip

    def run(self):
        url = f"http://{self.camera_ip}:4747/video"
        capture = cv2.VideoCapture(r"C:\Users\hamza\Videos\Video_FR_06_07_2023\Left_Camera\VID_20230706_143700.mp4")

        # Initialize variables for FPS calculation
        frame_count = 0
        start_time = cv2.getTickCount()

        while True:
            success, frame = capture.read()
            if success is False:
                break

            # Increment the frame number as a frame is being read by the program
            frame_count += 1
            # Calculate elapsed time
            elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

            # Check if one second has elapsed
            if elapsed_time >= 1.0:
                # Calculate FPS
                fps = f"FPS: {(frame_count / elapsed_time):.2f}"
                print(fps)
                # Reset variables for the next calculation
                frame_count = 0
                start_time = cv2.getTickCount()

            # Process the frame as needed (e.g. display, save, etc.)
            SHARED_BUFFER.put(frame)
            consumer_process = multiprocessing.Process(target=read_frames)
            consumer_process.start()


def create_thread():
    # Create a start a separate thread for each camera
    for ip in camera_ips:
        thread = CameraStream(ip)
        thread.start()

