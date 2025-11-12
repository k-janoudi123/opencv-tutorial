import cv2
import numpy as np


img = cv2.imread("assets/chess-board.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# img is source image , 100 is the maximum number of corners to be detected,
#  0.01 is the quality level, 10 is the minimum distance between corners
corners = cv2.goodFeaturesToTrack(img, 100, 0.01, 10)
corners = np.intp(corners)

for corner in corners:
    x,y = corner.ravel()
    cv2.circle(img, (x, y), 5, 255, -1)

print(img.shape)
print(corners)

cv2.imshow("Chess-Board", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
