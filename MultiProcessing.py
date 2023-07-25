import multiprocessing
import time

from MultipleIPCameras import create_thread
from LiveStreaming import read_frames
from SharedBuffer import MULTIPROCESS_SHARED_BUFFER


if __name__ == "__main__":
    # # Get CPU usage per core
    # cpu_percent = psutil.cpu_percent(interval=10, percpu=True)
    # # print(f"CPU Usage: {cpu_percent}")
    # # cpu_percent = None
    # # for i in range(10):
    # #     cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    # #     print(f"CPU Usage: {cpu_percent}")
    #
    # # Sort the CPU usage per core in ascending order
    # sorted_cores = sorted(enumerate(cpu_percent), key=lambda x: x[1])
    #
    # # Select the two cores with the minimum usage
    # min_usage_cores = sorted_cores[:2]
    # # print(min_usage_cores)
    #
    # # Select CPU core for the producer process
    # producer_core = min_usage_cores[0][0]
    # # print(f"Producer Core: {producer_core}")
    #
    # # Select CPU core for the consumer process
    # consumer_core = min_usage_cores[1][0]
    # # print(f"Consumer Core: {consumer_core}")

    start_time = time.time()

    producer_process = multiprocessing.Process(target=create_thread, args=(MULTIPROCESS_SHARED_BUFFER,))
    consumer_process = multiprocessing.Process(target=read_frames, args=(MULTIPROCESS_SHARED_BUFFER,))

    # Start the processes
    producer_process.start()
    # time.sleep(60)
    consumer_process.start()

    # # Set the CPU affinity for each process
    # producer_affinity = psutil.Process(producer_process.pid)  # .cpu_affinity([producer_core])
    # producer_affinity.cpu_affinity([producer_core])
    # # print(f"CPU Affinity for Producer Process: {producer_affinity.cpu_affinity()}")
    # consumer_affinity = psutil.Process(consumer_process.pid)  # .cpu_affinity([consumer_core])
    # consumer_affinity.cpu_affinity([consumer_core])
    # # print(f"CPU Affinity for Consumer Process: {consumer_affinity.cpu_affinity()}")

    # cpu_percent = psutil.cpu_percent(interval=10, percpu=True)
    # print(f"CPU Usage: {cpu_percent}")
    # for i in range(10):
    #     cpu_percent = psutil.cpu_percent(interval=10, percpu=True)
    #     print(f"CPU Usage: {cpu_percent}")
    #
    # print(f"CPU Affinity for Producer Process: {producer_affinity.cpu_affinity()}")
    # print(f"CPU Affinity for Consumer Process: {consumer_affinity.cpu_affinity()}")

    # Wait for both processes to finish
    producer_process.join()
    consumer_process.join()

    end_time = time.time()
    multi_processing_execution_time = int(end_time - start_time)

    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")
    print(f"Multi-Processing execution time: {multi_processing_execution_time // 60} minutes and {multi_processing_execution_time % 60} seconds")
