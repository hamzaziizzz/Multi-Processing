import multiprocessing
import queue

MULTIPROCESS_SHARED_BUFFER = multiprocessing.Queue()
MULTITHREAD_SHARED_BUFFER = queue.Queue()
