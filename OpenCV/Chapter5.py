# Warping perspective
import cv2
import numpy as np

img = cv2.imread("Resources/cards.jpg")
# img = cv2.resize(img, (1000, 620))
width, height = 250, 300
# 370,252 537,182 630,400 460,460
pts1 = np.float32([[370, 252], [537, 182], [630, 400], [460, 460]])
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))
cv2.imshow("Image", img)
cv2.imshow("Output", imgOutput)
cv2.waitKey(0)
