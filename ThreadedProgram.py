import threading
import time

from MultipleIPCameras import create_thread
from LiveStreaming import read_frames
from SharedBuffer import SHARED_BUFFER


if __name__ == "__main__":
    start_time = time.time()

    producer_thread = threading.Thread(target=create_thread, args=(SHARED_BUFFER,))
    consumer_thread = threading.Thread(target=read_frames, args=(SHARED_BUFFER,))

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
    print(f"Threading execution time: {threading_execution_time // 60} minutes and {threading_execution_time % 60} seconds")
