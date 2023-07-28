from confluent_kafka import Producer
import cv2
import time
import threading

from parameters import IP_CAMERAS, FRAME_WIDTH, FRAME_HEIGHT, IP_CAM_REINIT_WAIT_DURATION
from utils import roi_face_detection, create_mask
from custom_logging import logger

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker address
}

# Kafka topic for frames
kafka_topic_prefix = 'camera_frames_'

# Create Kafka producer
producer = Producer(kafka_conf)


class CameraStream:
    def __init__(self, camera_name: str, camera_ip: str):
        self.frame = None
        self.camera_name = camera_name
        self.camera_ip = camera_ip
        self.stream = cv2.VideoCapture(self.camera_ip)
        self.grabbed, _ = self.stream.read()
        self.initialized = self.grabbed
        self.process_this_frame = True
        if not self.grabbed:
            logger.error(f'Camera stream from {self.camera_name} (url: {self.camera_ip})) unable to initialize')
        else:
            logger.info(f'Camera stream from {self.camera_name} (url: {self.camera_ip}) initialized')

    def _read_frame(self):
        """
        Reads a frame from the stream
        """
        self.grabbed, self.frame = self.stream.read()

    def _discard_frame(self):
        """
        Reads and discards one frame
        """
        _, _ = self.stream.read()

    def release(self):
        """Releases the camera stream"""
        self.stream.release()

    def place_frame_in_kafka(self):
        if self.process_this_frame:
            self._read_frame()
            if not self.grabbed:
                # if the frame was not grabbed, then we have reached the end of the stream
                logger.error(
                    f'Could not read a frame from the camera stream from {self.camera_name} (url: {self.camera_ip})). Releasing the stream...')
                self.release()
                self.initialized = False
            else:
                # Resize the frame if the frame size is larger than the frame size specified in parameters.py
                self.frame = cv2.resize(self.frame, (FRAME_WIDTH, FRAME_HEIGHT))

                # Separate Region of Interest from the frame
                roi_width, roi_height, roi_x, roi_y = IP_CAMERAS[self.camera_name][1]
                roi_left, roi_top, roi_right, roi_bottom = roi_face_detection(
                    roi_width,
                    roi_height,
                    self.frame.shape[1],
                    self.frame.shape[0],
                    roi_x,
                    roi_y
                )
                mask = create_mask(self.frame, roi_left, roi_top, roi_right, roi_bottom)
                # Apply mask to the frame
                self.frame = self.frame * mask

                # Convert the frame to bytes
                _, frame_data = cv2.imencode(".jpg", self.frame)
                frame_data = frame_data.tobytes()

                # Send the frame to Kafka
                topic = kafka_topic_prefix + self.camera_name
                producer.produce(topic, value=frame_data)
                producer.flush()
        else:
            self._discard_frame()

        # toggle the flag to process alternate frames to improve the performance
        self.process_this_frame = not self.process_this_frame


def create_camera(name, ip):
    camera = CameraStream(camera_name=name, camera_ip=ip)

    while True:
        if camera.initialized:
            try:
                camera.place_frame_in_kafka()
            except Exception as exception:
                logger.error(
                    f"Exception raised while placing the frame in the buffer from {camera.camera_name} (url: {camera.camera_ip})). Releasing the stream...")
                camera.stream.release()
                camera.is_initialized = False
        else:
            logger.error(
                f"Camera stream from {camera.camera_name} (url: {camera.camera_ip})) is not accessible. Destroying the camera object...")
            del camera
            logger.info(
                f"Putting the thread to sleep for {name} (url: {ip})) for {IP_CAM_REINIT_WAIT_DURATION} seconds...")
            time.sleep(IP_CAM_REINIT_WAIT_DURATION)
            logger.info(f'Creating a new camera object for {name} (url: {ip}))...')
            camera = CameraStream(camera_name=name, camera_ip=ip)

def main():
    print("Process 1 Started")
    for camera_name in IP_CAMERAS:
        camera_ip = IP_CAMERAS[camera_name][0]
        camera_thread = threading.Thread(target=create_camera, args=(camera_name, camera_ip))
        camera_thread.start()
