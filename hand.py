import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Parameters
width, height = 1280, 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get the frames from the webcam
    success, img = cap.read()

    # Find hands
    hands, img = detector.findHands(img)

    # Prepare data to send
    data = []

    # If hands are detected
    if hands:
        # Get the first hand
        hand = hands[0]

        # Get the landmark list
        lmList = hand['lmList']

        # Extract x, y, z coordinates for each landmark
        for lm in lmList:
            x, y, z = lm
            data.extend([x, height - y, z])  # Adjust y-coordinate for correct orientation

        # Send the data to the server
        sock.sendto(str.encode(str(data)), serverAddressPort)
    img=cv2.resize(img, (0, 0), None, 0.5, 0.5);
    
    # Display the image
    cv2.imshow("Image", img)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the socket
cap.release()
cv2.destroyAllWindows()
sock.close()