import cv2
import numpy as np
import time
import POSEMODULE as pm  # Ensure POSEMODULE.py is in the same directory

cap = cv2.VideoCapture("video1.mp4")
detector = pm.PoseDetector()

curls_count = 0
direction = 0  # 0 = waiting, 1 = going down, 2 = going up

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (1000, 720))
    img = detector.findPose(img, False)
    lmList = detector.getPosition(img, False)

    if len(lmList) != 0:
        curls_angle = detector.findAngle(img, 12, 14, 16)  # Shoulder, Elbow, Wrist
        
        # Check for downward movement
        if curls_angle > 160:
            if direction == 2:  # Was moving up before
                curls_count += 1  # Count curl only when full motion is completed
            direction = 1  # Now moving down
        
        # Check for upward movement
        elif curls_angle < 70:
            direction = 2  # Now moving up

    # Display count on the screen
    cv2.putText(img, f'Curls: {curls_count}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("AI GYM TRAINER", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
