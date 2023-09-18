import cv2

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Set the frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()

    if not ret:
        print('Error: Could not read frame.')
        break

    cv2.imshow("Reaction Game", frame)  
    
    k = cv2.waitKey(1) & 0xFF 
    if k == ord('q'):
        break

from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    frame = cap.read()
    hands, frame = detector.findHands(frame, flipType=False)
    cv2.imshow("Reaction Game", frame)

