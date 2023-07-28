import cv2


def read_frames(shared_buffer):
    # # Initialize variables for FPS calculation
    # start_time = cv2.getTickCount()
    
    while True:
        frame = shared_buffer.get()
    
        if frame is None:
            break
    
        # fact = 1
        # for i in range(1, 501):
        #     fact *= i
    
        # end_time = cv2.getTickCount()
        # # Calculate elapsed time
        # elapsed_time = (end_time - start_time) / cv2.getTickFrequency()

        # # Calculate FPS
        # fps = f"FPS: {(1 / elapsed_time):.2f}"
        #
        # cv2.rectangle(frame, (0, 0), (170, 50), (0, 0, 0), -1)
        # cv2.putText(frame, fps, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
        # Display the frame
        cv2.imshow("IP Camera Footage", frame)
    
        # start_time = cv2.getTickCount()
    
        # Exit the program if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    
    # Destroy all windows when done
    cv2.destroyAllWindows()


def main(shared_buffer):
    print("Process 2 Started")
    read_frames(shared_buffer)
