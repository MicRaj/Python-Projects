# Drawing shapes
import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)

# print(img)
# img[200:300, 100:300] = 255, 0, 0  # BGR

cv2.line(img, (0, 0), (img.shape[0], img.shape[1]), (0, 255, 0), 3)
cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), cv2.FILLED)
cv2.circle(img, (400, 50), 30, (255, 255, 0))
cv2.putText(img, "OPENCV", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 1)
cv2.imshow("Image", img)
cv2.waitKey(0)
