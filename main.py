import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Set the frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = HandDetector(detectionCon=0.6, maxHands=2)

while True:
    frame = cap.read()[1]  # Read the frame directly, without using ret

    hands, frame = detector.findHands(frame, flipType=False)
    if hands:
        print(f"Detected {len(hands)} hand(s)")

    cv2.imshow("Reaction Game", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
