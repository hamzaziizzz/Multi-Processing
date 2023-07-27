from confluent_kafka import Producer
from threading import Thread
import cv2

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker address
}

# Kafka topic for frames
kafka_topic = 'camera_frames'

# Create Kafka producer
producer = Producer(kafka_conf)

# Define the camera IP addresses
camera_ips = [
    "http://192.168.21.115:5000",
    "http://192.168.21.115:5010",
    "http://192.168.21.115:5020"
]


def send_frame_to_kafka(frame_data):
    producer.produce(kafka_topic, value=frame_data)
    producer.flush()


def camera_producer(camera_ip):
    capture = cv2.VideoCapture(camera_ip)

    while True:
        success, frame = capture.read()
        if not success:
            break

        # Resize the frame
        frame = cv2.resize(frame, (1280, 768))

        # Encode the frame as bytes
        _, frame_data = cv2.imencode(".jpg", frame)
        frame_data = frame_data.tobytes()

        # Send the frame to Kafka
        send_frame_to_kafka(frame_data)

    # Release the video capture
    capture.release()
    send_frame_to_kafka(None)


def main():
    # Create and start camera producer threads
    camera_threads = [Thread(target=camera_producer, args=(ip,)) for ip in camera_ips]

    for thread in camera_threads:
        thread.start()

    for thread in camera_threads:
        thread.join()


if __name__ == "__main__":
    main()
