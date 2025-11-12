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

    # Draw a blue diagonal line across the frame
    # frame is the source image, (0,0) is the starting point,
    #  (width, height) is the ending point, (255,0,0) is the color (blue in BGR),
    #  and 5 is the thickness of the line
    # the two lines will form an X across the frame
    cv2.line(frame, (0, 0), (width, height), (255, 0, 0), 5)

    cv2.line(frame, (0, height), (width, 0), (0, 255, 0), 5)

    # drawing a square

    cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 3)

    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(
        frame, "OpenCV Demo", (5, height - 50), font, 5, (255, 255, 255), 2, cv2.LINE_AA
    )

    # (50, height-50) is the position where the text starts

    # 5 is the font scale

    # (255, 255, 255) is the color (white in BGR)

    # 2 is the thickness

    # cv2.LINE_AA is the line type

    cv2.imshow("Frame", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


## Visual Representation
# ```
# ┌──────────────────────────────────┐  ← y = 0 (top)
# │                                  │
# │  (50, 50) ← text here            │
# │                                  │
# │                                  │
# │                                  │
# │                                  │
# │                                  │
# │                                  │
# │                                  │
# │  (5, height-50) ← text here      │  ← y = 430 (50px from bottom)
# └──────────────────────────────────┘  ← y = 480 (bottom)
#    x=5                          x=640
# ```
