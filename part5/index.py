import cv2
import numpy as np


# Initialize video capture from the default camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = (
        cap.read()
    )  # ret is a boolean indicating if the frame was read correctly
    if not ret:  # if the frame was not read correctly
        break
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the blue color range in HSV
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for blue color

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image to extract the blue regions
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Frame", result)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
