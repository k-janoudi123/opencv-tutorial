import cv2

img = cv2.imread("assets/photo.jpeg")
img = cv2.resize(img, (600, 400))

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

cv2.imwrite("assets/photo_modified2.jpeg", img)



cv2.imshow("Image", img)

cv2.waitKey(0)

cv2.destroyAllWindows()

