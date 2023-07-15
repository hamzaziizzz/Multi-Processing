import cv2
from SharedBuffer import SHARED_BUFFER


def read_frames():
    # Initialize variables for FPS calculation
    start_time = cv2.getTickCount()

    while not SHARED_BUFFER.empty():
        frame = SHARED_BUFFER.get()
        frame = cv2.resize(frame, (1280, 768))

        end_time = cv2.getTickCount()
        # Calculate elapsed time
        elapsed_time = (end_time - start_time) / cv2.getTickFrequency()

        # Calculate FPS
        fps = f"FPS: {(1 / elapsed_time):.2f}"

        cv2.rectangle(frame, (0, 0), (170, 50), (0, 0, 0), -1)
        cv2.putText(frame, fps, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow("Camera", frame)

        start_time = cv2.getTickCount()

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
