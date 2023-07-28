import threading
import time
from kafka_producer import main as producer_main
from kafka_consumer import main as consumer_main

if __name__ == "__main__":
    start_time = time.time()

    producer_thread = threading.Thread(target=producer_main)
    consumer_thread = threading.Thread(target=consumer_main)

    # Start the processes
    producer_thread.start()
    # time.sleep(60)

    consumer_thread.start()

    # Wait for both processes to finish
    producer_thread.join()
    consumer_thread.join()

    end_time = time.time()
    threading_execution_time = int(end_time - start_time)

    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")
    print(f"Kafka execution time: {threading_execution_time // 60} minutes and {threading_execution_time % 60} seconds")
