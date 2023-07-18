# Multi-Processing in Python

This repository comprises four Python scripts: MultipleIPCameras.py, LiveStreaming.py, SharedBuffer.py, and MultiProcessing.py. Each script serves a specific purpose within the project.

- `MultipleIPCameras.py` and `LiveStreaming.py` are the **producer** and **consumer processes**, respectively. The producer process (MultipleIPCameras.py) is responsible for capturing frames of IP Cameras, while the consumer process (LiveStreaming.py) display those frames.

- `SharedBuffer.py` facilitates inter-process communication between the producer and consumer processes. It enables the exchange of frames between these two components by putting the captured frames into the **SHARED_BUFFER** captured by the producer process and providing those frames as input to the consumer process.

- Finally, the **main script**, `MultiProcessing.py`, serves as the entry point for the program. It is responsible for initiating the execution of the project and orchestrating the interaction between the various scripts.

By following the guidelines outlined in this repository, individuals can effectively utilize these scripts to begin working on the project.

## Step 1: Creating Virtual Environment

```bash
python3 -m venv venv/
```

## Step 2: Activating Virtual Environment

```bash
source venv/bin/activate
```

## Step 3: Installing Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Executing the Program

```bash
python3 MultiProcessing.py
```
