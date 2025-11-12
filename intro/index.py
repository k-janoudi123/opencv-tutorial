import cv2
import numpy as np

img = cv2.imread("assets/photo.jpeg")

print(type(img))  # <class 'numpy.ndarray'>
print(img.shape)  # (3999, 5999, 3)
print(img.dtype)  # uint8 (values from 0-255)

## How it's organized:

# [
#   [  # Row 0 (top row)
#     [B, G, R],  # Pixel (0, 0) - top-left corner
#     [B, G, R],  # Pixel (0, 1)
#     [B, G, R],  # Pixel (0, 2)
#     ...         # 5999 pixels across
#   ],
#   [  # Row 1
#     [B, G, R],  # Pixel (1, 0)
#     [B, G, R],  # Pixel (1, 1)
#     ...
#   ],
#   ...  # 3999 rows down
# ]


