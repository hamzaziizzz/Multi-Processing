import multiprocessing
import time

from MultipleIPCameras import *

if __name__ == "__main__":
    freeze_support()
    producer_process = multiprocessing.Process(target=create_thread)
    producer_process.start()
