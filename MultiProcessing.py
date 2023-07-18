import multiprocessing

from MultipleIPCameras import create_thread
from LiveStreaming import read_frames
from SharedBuffer import SHARED_BUFFER

if __name__ == "__main__":
    producer_process = multiprocessing.Process(target=create_thread, args=(SHARED_BUFFER, ))
    consumer_process = multiprocessing.Process(target=read_frames, args=(SHARED_BUFFER, ))

    producer_process.start()
    consumer_process.start()

    # Wait for both processes to finish
    producer_process.join()
    consumer_process.join()
