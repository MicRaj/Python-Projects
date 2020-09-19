# cv2 Functions
import cv2
import numpy as np

# IMG manipulation
img = cv2.imread("Resources/pic.jpg")
kernel = np.ones((5, 5), np.uint8)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converts to gray scale
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
imgBlur2 = cv2.GaussianBlur(imgGray, (13, 13), 0)  # More Blurred
imgCanny = cv2.Canny(img, 150, 200)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
imgErode = cv2.erode(imgDilation, kernel, iterations=1)

cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image", imgBlur)
# cv2.imshow("Blur Image 2", imgBlur2)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dilation Image", imgDilation)
cv2.imshow("Eroded Image", imgErode)
cv2.waitKey(0)
