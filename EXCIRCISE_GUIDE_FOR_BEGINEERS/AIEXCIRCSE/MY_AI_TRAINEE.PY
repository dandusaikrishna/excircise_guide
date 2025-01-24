import cv2
import numpy as np
import time
import exera as pm

cap = cv2.VideoCapture("jumps.mp4")
detector = pm.PoseDetector()

min_val = 1000
max_val = 0
filled_rect_bottom_y = 0
squats_cnt = 0
pushup_count = 0
curls_count = 0
dir_pushup = 0
jump_count = 0
ptime = 0
color = (0, 0, 255)

last_squat_time = time.time()
squat_paused = False
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (1000, 720))
    
    img = detector.findPose(img, False)
    lmList = detector.getPosition(img, False)
    
    # print(lmList)
    
    if len(lmList) != 0:
        dist_from_gnd = detector.distance(img, 20, 18, 8)
        dist_from_gnd_to_head = detector.findDistance(0,32,img)

        distance_elbow_knee = detector.findDistance(13, 25, img)
        # Right Arm for curls
        curls_angle = detector.findAngle(img, 12, 14, 16)
        # Update curls count
        if (25 < curls_angle < 180) and  (5 < dist_from_gnd < 12) :
            new_curls_angle = 180 - curls_angle
            curls_per = np.interp(curls_angle, (120, 170), (0, 100))
            filled_rect_bottom_y = 400 - int(new_curls_angle * 2)

            cv2.rectangle(img, (800, 100), (900, 450), (0, 255, 0), 4)  # Outline rectangle with fixed length and width
            cv2.rectangle(img, (800, filled_rect_bottom_y), (900, 450), (0, 0, 255), cv2.FILLED)

            # filled_rect_bottom_y = 400 - int(curl * 3)
            if curls_per == 100 and dir_pushup == 0:
                curls_count += 0.5
                dir_pushup = 1
            elif curls_per == 0 and dir_pushup == 1:
                curls_count += 0.5
                dir_pushup = 0


        #update pushups count
        if int(19) < dist_from_gnd:
            a1 = detector.findAngle(img, 12, 14, 16, False)
            a2 = detector.findAngle(img, 15, 13, 11, False)

            # Interpolate angles to percentage values
            per_val1 = int(np.interp(a1, (85, 165), (100, 0)))
            per_val2 = int(np.interp(a2, (85, 165), (100, 0)))
            filled_rect_bottom_y = 400 - int(per_val1 * 3)

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



        #update squats count

        # print(dist_from_gnd_to_head[0])
        if 170 < dist_from_gnd_to_head[0] < 330:
            # Convert distance to percentage between 0% and 100%
            percentage = np.interp(distance_elbow_knee[0], [50, 200], [0, 100])
            print(percentage)
            bar = int(percentage)
            filled_rect_bottom_y = 400 - int(bar * 4)
            # min_per = min(percentage,min_per)
            # max_per = max(percentage,max_per)
        # Update squats count based on percentage change
            if percentage < 8:
                current_time = time.time()
                if not squat_paused:  # Check if squat count is not paused
                    squats_cnt += 1
                    bar = 400
                    last_squat_time = current_time  # Update last squat time
                    squat_paused = True  # Pause the squat count
                elif current_time - last_squat_time >= 2:  # Check if 1 second has passed since last squat count increase
                    squat_paused = False
        # x = detector.findDistance(32,31,img)
        # print(x)
        
            
        # Calculate the y-coordinate of the bottom of the filled rectangle
        cv2.rectangle(img, (800, 100), (900, 450), (0, 255, 0), 4)  # Outline rectangle with fixed length and width
        cv2.rectangle(img, (800, filled_rect_bottom_y), (900, 450), (0, 0, 255),cv2.FILLED)  # Filled rectangle with color based on percentage

        cv2.putText(img, f'Curls: {int(curls_count)}', (45, 670), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv2.putText(img, f'Pushups: {int(pushup_count)}', (45, 720), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
        cv2.putText(img, f'Squats: {int(squats_cnt)}', (45, 630), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
        # cv2.putText(img, f'Jump: {int(jump_count)}', (45, 600), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    # Calculate and display the frame rate
    # cTime = time.time()
    # fps = 1 / (cTime - ptime)
    # ptime = cTime
    # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("AI GYM TRAINER", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# print(min_val,max_val)
# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
