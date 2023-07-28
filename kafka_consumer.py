from confluent_kafka import Consumer, KafkaError
import cv2
import numpy as np

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker address
    'group.id': 'camera_consumer_group',    # Consumer group ID
    'auto.offset.reset': 'earliest'        # Start reading from the beginning of the topic
}

# Kafka topic for frames
kafka_topic = 'camera_frames'

# Create Kafka consumer
consumer = Consumer(kafka_conf)
consumer.subscribe([kafka_topic])


def read_frames():
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            break

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("Reached end of partition")
            else:
                print(f"Error while consuming: {msg.error()}")
        else:
            # Decode the frame data
            frame_data = msg.value()

            # Convert the frame data back to an image
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

            # Process the frame as needed (e.g., display, save, etc.)
            cv2.imshow("IP Camera Footage", frame)

            # Exit the program if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break

    # Destroy all windows when done
    cv2.destroyAllWindows()


def main():
    read_frames()
