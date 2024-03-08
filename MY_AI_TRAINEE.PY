import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("2WORKS.mp4")
detector = pm.poseDetector()

pushup_count = 0
curls_count = 0
dir_pushup = 0
ptime = 0
color = (0, 0, 255)
bar = 700
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (1000, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        # Right Arm for curls
        curls_angle = detector.findAngle(img, 12, 14, 16)
        # left arm
        curls_angle = detector.findAngle(img, 11, 13, 15)

        # Left Arm for pushups
        pushup_angle = detector.findAngle(img, 11, 13, 15)

        # Update curls count
        if 25 < curls_angle < 180:
            curls_per = np.interp(curls_angle, (120, 170), (0, 100))
            curls_bar = np.interp(curls_angle, (120, 170), (900, 100))
            if curls_per == 100 and dir_pushup == 0:
                curls_count += 0.5
                bar = 200
                dir_pushup = 1
            elif curls_per == 0 and dir_pushup == 1:
                curls_count += 0.5
                bar = 400
                dir_pushup = 0


        # Update pushups count
        dist_from_gnd = detector.distance(img, 19, 17, 7)
        dist_from_gnd = detector.distance(img, 20, 18, 8)

        # print('DIST:', dist_from_gnd)
        if int(18) < dist_from_gnd:
            a1 = detector.findAngle(img, 12, 14, 16, False)
            a2 = detector.findAngle(img, 15, 13, 11, False)

            # Interpolate angles to percentage values
            per_val1 = int(np.interp(a1, (85, 165), (100, 0)))
            per_val2 = int(np.interp(a2, (85, 165), (100, 0)))

            # Update push-ups count based on angle thresholds
            if per_val1 == 100 and per_val2 == 100:
                if dir_pushup == 0:
                    pushup_count += 1
                    dir_pushup = 1
                    color = (0, 255, 0)
            elif per_val1 == 0 and per_val2 == 0:
                if dir_pushup == 1:
                    dir_pushup = 0
                    color = (0, 255, 0)


        cv2.rectangle(img, (1100, 200), (1200, 700), (0, 255, 0), 4)
        cv2.rectangle(img, (1100, int(bar)), (1200, 700), (0, 255, 255), cv2.FILLED)
        cv2.putText(img, f'Curls: {int(curls_count)}', (45, 670), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv2.putText(img, f'Pushups: {int(pushup_count)}', (45, 720), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    # Calculate and display the frame rate
    # cTime = time.time()
    # fps = 1 / (cTime - ptime)
    # ptime = cTime
    # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("AI GYM TRAINER", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
