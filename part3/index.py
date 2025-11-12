# this just captures video from the webcam and displays it in a window

# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read() # ret is a boolean indicating if the frame was read correctly
#     if not ret:     # if the frame was not read correctly
#         break
#     cv2.imshow("Frame", frame)

#     if cv2.waitKey(1) == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()

#########################################


import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = (
        cap.read()
    )  # ret is a boolean indicating if the frame was read correctly
    if not ret:  # if the frame was not read correctly
        break

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Width: {width}, Height: {height}")
    # creating a black frame
    img = np.zeros(frame.shape, dtype=np.uint8)
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # placing the smaller frame in each quadrant
    # Top-left quadrant (rows: 0 to half, cols: 0 to half)
    img[: height // 2, : width // 2] = smaller_frame
    # Bottom-left quadrant (rows: half to end, cols: 0 to half)
    img[height // 2 :, : width // 2] = smaller_frame
    # Top-right quadrant (rows: 0 to half, cols: half to end)
    img[: height // 2, width // 2 :] = smaller_frame
    # Bottom-right quadrant (rows: half to end, cols: half to end)
    img[height // 2 :, width // 2 :] = smaller_frame

    cv2.imshow("Frame", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


# **Visual representation:**
# ```
# +----------------+----------------+
# |                |                |
# |   Top-Left     |   Top-Right    |    
# |  [:h//2,       |  [:h//2,       |
# |   :w//2]       |   w//2:]       |
# |                |                |
# +----------------+----------------+
# |                |                |
# |  Bottom-Left   |  Bottom-Right  |
# |  [h//2:,       |  [h//2:,       |
# |   :w//2]       |   w//2:]       |
# |                |                |
# +----------------+----------------+
