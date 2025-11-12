import cv2

img = cv2.imread("assets/blue-image.png")

# Make the top 100 rows red
for i in range(100): # rows
    for j in range(img.shape[1]): # columns
        img[i, j] = [0, 0, 255]

print(img.shape)
# img = cv2.resize(img, (600, 400), img)

print(img.shape)  # (400, 600, 3)

# cv2.imshow("Modified Image", img)


#now let's crop a section of the image
# Crop a rectangle from (200, 0) to (450, 100)
tag = img[0:100, 200:450]
# from row 0 to row 100, from column 200 to column 450

# paste the cropped section onto the original image at (200, 0)
img[200:300, 0:250] = tag

cv2.imshow("Tag", tag)

cv2.imshow("Modified Image", img)

cv2.waitKey(0)

cv2.destroyAllWindows()
