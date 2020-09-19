# img ,video and webcam
import cv2

print("Package Imported")

# Image
img = cv2.imread("Resources/pic.jpg")
cv2.imshow("Output", img)
cv2.waitKey(1000)

# Video
# cap = cv2.VideoCapture("Resources/vid.mp4")
cap = cv2.VideoCapture(0)  # Uses Webcam
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height
cap.set(10, 100)  # Brightness
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Waits for q press
        break