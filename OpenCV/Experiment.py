import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # Uses Webcam
kernel = np.ones((2, 2), np.uint8)

img = cv2.imread("Resources/sudoku.png")
imgCanny = cv2.Canny(img, 200, 200)
imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
cv2.imshow("Image", img)
cv2.imshow("Image Canny", imgCanny)
cv2.imshow("Image DIl", imgDil)
cv2.waitKey(0)

# while True:
#     success, img = cap.read()
#
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img = cv2.Canny(img, 100, 100)
#     img = cv2.dilate(img, kernel, iterations=1)
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Waits for q press
#         break
