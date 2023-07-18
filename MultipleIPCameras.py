import cv2
from threading import Thread

# Define the camera IP addresses
camera_ips = [
    "http://192.168.17.158:4747/video",
    "http://192.168.16.232:4747/video",
    "http://192.168.3.223:4747/video"
]


# def run():
#     # url = f"http://{self.camera_ip}:4747/video"
#     capture = cv2.VideoCapture(
#         r"C:\Users\hamza\Videos\Video_FR_06_07_2023\Left_Camera\VID_20230706_143700.mp4")

#     # Initialize variables for FPS calculation
#     frame_count = 0
#     start_time = cv2.getTickCount()

#     while True:
#         success, frame = capture.read()
#         if success is False:
#             break

#         # Increment the frame number as a frame is being read by the program
#         frame_count += 1
#         # Calculate elapsed time
#         elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

#         # Check if one second has elapsed
#         if elapsed_time >= 1.0:
#             # Calculate FPS
#             fps = f"FPS: {(frame_count / elapsed_time):.2f}"
#             print(fps)
#             # Reset variables for the next calculation
#             frame_count = 0
#             start_time = cv2.getTickCount()

#         # Process the frame as needed (e.g. display, save, etc.)
#         SHARED_BUFFER.put(frame)

#     # Release the video capture and signal the end of frames
#     capture.release()
#     SHARED_BUFFER.put(None)


# Define a class to handle camera streaming in a separate thread
class CameraStream(Thread):
    def __init__(self, camera_ip: str, shared_buffer):
        Thread.__init__(self)
        self.camera_ip = camera_ip
        self.shared_buffer = shared_buffer

    def run(self):
        # capture = cv2.VideoCapture(r"C:\Users\hamza\Videos\Video_FR_06_07_2023\Left_Camera\VID_20230706_143700.mp4")
        capture = cv2.VideoCapture(self.camera_ip)

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
            self.shared_buffer.put(frame)

        # Release the video capture and signal the end of frames
        capture.release()


def create_thread(shared_buffer):
    # Create a start a separate thread for each camera
    for ip in camera_ips:
        thread = CameraStream(ip, shared_buffer)
        thread.start()
        # thread.join()
