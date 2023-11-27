import cv2

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video_input/output.avi', fourcc, 20.0, (640,  480))

# Capture video from the webcam
cap = cv2.VideoCapture(2)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything when job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
