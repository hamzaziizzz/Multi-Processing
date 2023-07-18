import multiprocessing
import psutil

from MultipleIPCameras import create_thread
from LiveStreaming import read_frames
from SharedBuffer import SHARED_BUFFER

if __name__ == "__main__":
    producer_process = multiprocessing.Process(target=create_thread, args=(SHARED_BUFFER, ))
    consumer_process = multiprocessing.Process(target=read_frames, args=(SHARED_BUFFER, ))

    # Set the CPU affinity for each process
    producer_affinity = psutil.Process(producer_process.pid)
    producer_affinity.cpu_affinity([1])  # Set process 1 to run on CPU core 1

    consumer_affinity = psutil.Process(consumer_process.pid)
    consumer_affinity.cpu_affinity([2, 3, 4])  # Set process 2 to run on CPU core 2, core 3 and core 4
    
    # Start the processes
    producer_process.start()
    consumer_process.start()

    # Wait for both processes to finish
    producer_process.join()
    consumer_process.join()
