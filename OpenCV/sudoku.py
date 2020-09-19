import cv2
import numpy as np

img = cv2.imread('Resources/sudoku2.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(img, (13, 13), 2)  # Get rid of noise
imgCanny = cv2.Canny(img, 100, 100)
outerbox = np.zeros_like(img)
imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

cv2.imshow("Image", imgThresh)
cv2.imshow("Image Canny", imgCanny)
cv2.waitKey(0)
