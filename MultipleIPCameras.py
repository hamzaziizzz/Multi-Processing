import cv2
from threading import Thread

# Define the camera IP addresses
camera_ips = [
    # "http://192.168.1.4:5000",
    # "http://192.168.21.115:5000",
    # "http://192.168.21.115:5010",
    # "http://192.168.21.115:5020"
    # "http://192.168.17.158:4747/video"
    # "http://192.168.18.197:4747/video",
    # "http://192.168.16.232:4747/video",
    # "http://192.168.3.223:4747/video",
    # "http://192.168.12.10:4747/video"
    # "http://192.168.18.61:4747/video"
]

MAXIMUM_SIZE = 1024


# Define a class to handle camera streaming in a separate thread
class CameraStream(Thread):
    def __init__(self, camera_ip: str, shared_buffer):
        Thread.__init__(self)
        self.camera_ip = camera_ip
        self.shared_buffer = shared_buffer

    def run(self):
        # capture = cv2.VideoCapture(r"C:\Users\hamza\Videos\Video_FR_06_07_2023\Left_Camera\VID_20230706_143700.mp4")
        capture = cv2.VideoCapture(self.camera_ip)

        # # Initialize variables for FPS calculation
        # frame_count = 0
        # start_time = cv2.getTickCount()

        while True:
            success, frame = capture.read()
            if success is False:
                break

            # Resize the frame
            frame = cv2.resize(frame, (1280, 768))

            # # Reformat each frame as PNG file
            # _, frame = cv2.imencode(".jpg", frame)
            # frame = frame.tobytes()

            # Put some random text on the frame
            frame = cv2.putText(
                img=frame,
                text="Hamza Aziz",
                org=(70, 70),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=(0, 0, 255),
                thickness=2,
                lineType=cv2.LINE_AA
            )

            # fact = 1
            # for i in range(1, 501):
            #     fact *= i
            # print(fact)

            # # Increment the frame number as a frame is being read by the program
            # frame_count += 1
            # # Calculate elapsed time
            # elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            #
            # # Calculate FPS
            # fps = f"FPS: {(1 / elapsed_time):.2f}"
            # print(fps)

            # Process the frame as needed (e.g. display, save, etc.)
            if self.shared_buffer.qsize() < MAXIMUM_SIZE:
                # print(f"Current Queue Size: {self.shared_buffer.qsize()}")
                self.shared_buffer.put(frame)
            else:
                while not self.shared_buffer.empty():
                    self.shared_buffer.get()
                # raise ValueError("Queue has reached its maximum size.")

            # Exit the program if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break

            # start_time = cv2.getTickCount()

        # Release the video capture and signal the end of frames
        capture.release()
        self.shared_buffer.put(None)


def create_thread(shared_buffer):
    print("Process 1 Started")
    # Create a start a separate thread for each camera
    for ip in camera_ips:
        thread = CameraStream(ip, shared_buffer)
        thread.start()
        # thread.join()
