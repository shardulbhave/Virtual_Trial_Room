import os
import cv2
import mediapipe as mp
import cvzone
import time

'''
shirtFolderPath = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\MaleShirts"
listShirts = os.listdir(shirtFolderPath)
pantFolderPath = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\MalePants"
listPants = os.listdir(pantFolderPath)
'''
fixedRatio = 154 / 150  # width of shirt / width of points 11 and 12
shirtRatioHeightWidth = 581 / 440
fixedRatio1 = 400 / 150  # width of pant / width of points 23 and 24
PantRatioHeightWidth = 400 / 510
imgButtonMale = cv2.imread(
    "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\malebutton.png",
    cv2.IMREAD_UNCHANGED)
imgButtonFemale = cv2.imread(
    "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\femalebutton.png",
    cv2.IMREAD_UNCHANGED)
imgButtonReset = cv2.imread(
    "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\resetbutton.png",
    cv2.IMREAD_UNCHANGED)

# Threshold for finger up detection
FINGER_UP_THRESHOLD = 0.5  # Adjust this value as needed


def main():
    loopflag = 1
    resetflag = 0
    FemaleFlag = 0
    MaleFlag = 0
    counterReset = 0
    counterMale = 0
    counterFemale = 0
    selectionSpeed = 5
    imageNumber = 0
    nextShirt = 0
    nextPant = 0
    delay_duration = 0.5  # Adjust this value as needed

    medhands = mp.solutions.hands
    mp_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    mp_pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    current_shirt_index = 0
    current_pant_index = 0
    last_shirt_change_time = time.time()
    last_pant_change_time = time.time()
    fingercount = 0
    last_increment_time = time.time()
    last_decrement_time = time.time()
    next_shirt_incremented = False
    next_pant_incremented = False
    next_pant_decremented = False
    next_shirt_decremented = False

    while cap.isOpened() or loopflag == 1:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = mp_hands.process(rgb_frame)
        res_pose = mp_pose.process(rgb_frame)
        lmlist = []
        tipids = [4, 8, 12, 16, 20]  # list of all landmarks of the tips of fingers

        cv2.rectangle(frame, (10, 350), (120, 440), (0, 255, 204), cv2.FILLED)
        cv2.rectangle(frame, (10, 350), (120, 440), (0, 0, 0), 5)

        if res.multi_hand_landmarks:
            for handlms in res.multi_hand_landmarks:
                for id, lm in enumerate(handlms.landmark):

                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                    if len(lmlist) != 0 and len(lmlist) == 21:
                        fingerlist = []

                        # thumb and dealing with flipping of hands
                        if lmlist[12][1] > lmlist[20][1]:
                            if lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]:
                                fingerlist.append(1)
                            else:
                                fingerlist.append(0)
                        else:
                            if lmlist[tipids[0]][1] < lmlist[tipids[0] - 1][1]:
                                fingerlist.append(1)
                            else:
                                fingerlist.append(0)

                        # others
                        for id in range(1, 5):
                            if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:
                                fingerlist.append(1)
                            else:
                                fingerlist.append(0)

                        if len(fingerlist) != 0:
                            fingercount = fingerlist.count(1)

                        # cv2.putText(frame, str(fingercount), (25, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

                    # change color of points and lines
                    mp_drawing.draw_landmarks(frame, handlms, medhands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 255, 204), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=3))
        '''
        # fps counter
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime


        #fps display
        cv2.putText(frame, f'FPS:{str(int(fps))}', (0, 12), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

        cv2.imshow("hand gestures", frame)
        '''

        if res_pose.pose_landmarks:
            landmark_11 = res_pose.pose_landmarks.landmark[11]
            landmark_12 = res_pose.pose_landmarks.landmark[12]
            landmark_23 = res_pose.pose_landmarks.landmark[23]
            landmark_24 = res_pose.pose_landmarks.landmark[24]
            landmark_16 = res_pose.pose_landmarks.landmark[16]
            landmark_15 = res_pose.pose_landmarks.landmark[15]

            h, w, c = frame.shape
            x_11, y_11 = int(landmark_11.x * w), int(landmark_11.y * h)
            x_12, y_12 = int(landmark_12.x * w), int(landmark_12.y * h)

            widthOfShirt = int(1.55 * abs(x_11 - x_12) * fixedRatio)
            heightOfShirt = int(widthOfShirt * shirtRatioHeightWidth)

            h1, w1, c1 = frame.shape
            x_23, y_23 = int(landmark_23.x * w), int(landmark_23.y * h)
            x_24, y_24 = int(landmark_24.x * w), int(landmark_24.y * h)

            if landmark_15.y < 0.20 and landmark_15.x < 0.70:
                counterReset += 4
                cv2.ellipse(frame, (325, 50), (30, 30), 0, 0,
                            counterReset * selectionSpeed, (0, 255, 0), 16)
                if counterReset * selectionSpeed > 360 or counterReset * selectionSpeed == 360:
                    resetflag = 1
                    counterReset = 0

            elif landmark_16.y < 0.20:
                counterFemale += 4
                cv2.ellipse(frame, (55, 50), (30, 30), 0, 0,
                            counterFemale * selectionSpeed, (0, 255, 0), 16)
                if counterFemale * selectionSpeed > 360 or counterFemale * selectionSpeed == 360:
                    FemaleFlag = 1
                    counterFemale = 0

            elif landmark_15.y < 0.20:
                counterMale += 4
                cv2.ellipse(frame, (580, 50), (30, 30), 0, 0,
                            counterMale * selectionSpeed, (0, 255, 0), 16)
                if counterMale * selectionSpeed > 360 or counterMale * selectionSpeed == 360:
                    MaleFlag = 1
                    counterMale = 0


            else:
                counterMale = 0
                counterFemale = 0
                counterReset = 0
            widthOfPant = int(abs(x_23 - x_24) * fixedRatio1)
            heightOfPant = int(widthOfPant * PantRatioHeightWidth)

            print(fingercount)
            frame = cvzone.overlayPNG(frame, imgButtonReset, (295, 20))
            frame = cvzone.overlayPNG(frame, imgButtonMale, (550, 20))
            frame = cvzone.overlayPNG(frame, imgButtonFemale, (25, 20))
        if MaleFlag == 1:

            shirtFolderPath_male = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\MaleShirts"
            listShirts = os.listdir(shirtFolderPath_male)
            pantFolderPath_male = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\MalePants"
            listPants = os.listdir(pantFolderPath_male)
            # Use paths for male shirts and pants

            if fingercount == 1 and nextShirt + 1 < len(listShirts) and not next_shirt_incremented:
                if time.time() - last_increment_time >= delay_duration:
                    nextShirt += 1
                    next_shirt_incremented = True
                    last_increment_time = time.time()
            elif fingercount == 2 : #and not next_shirt_decremented:
                if time.time() - last_decrement_time >= delay_duration:
                    nextShirt -= 1
                    next_shirt_decremented = True
                    last_decrement_time = time.time()

            elif fingercount != 1:
                next_shirt_incremented = False

            elif fingercount != 2:
                next_shirt_decremented = False

            if fingercount == 4 and nextPant + 1 < len(listPants) and not next_pant_incremented:
                if time.time() - last_increment_time >= delay_duration:
                    nextPant += 1
                    next_pant_incremented = True
                    last_increment_time = time.time()

            if fingercount == 5 : # and not next_pant_decremented:
                if time.time() - last_decrement_time >= delay_duration:
                    nextPant -= 1
                    next_pant_decremented = True
                    last_decrement_time = time.time()

            if fingercount != 4:
                next_pant_incremented = False

            if fingercount != 5:
                next_pant_decremented = False

            imgPant = cv2.imread(os.path.join(pantFolderPath_male, listPants[nextPant]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.imread(os.path.join(shirtFolderPath_male, listShirts[nextShirt]), cv2.IMREAD_UNCHANGED)

            imgPant = cv2.resize(imgPant, (widthOfPant, int(2 * widthOfPant * PantRatioHeightWidth)))

            # Pant Offset
            x_offset1 = -50
            y_offset1 = -30
            frame = cvzone.overlayPNG(frame, imgPant, (x_24 + x_offset1, y_24 + y_offset1))

            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(1.05 * widthOfShirt * shirtRatioHeightWidth)))

            # Shirt offset
            x_offset = -35
            y_offset = -40
            frame = cvzone.overlayPNG(frame, imgShirt, (x_12 + x_offset, y_12 + y_offset))

            # cv2.putText(frame, str(fingercount), (25, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

            # Size Display
            ShirtSize = widthOfShirt * 0.119
            PantSize = widthOfPant * 0.240
            cv2.putText(frame, f"Shoulder Size: {ShirtSize:.2f}in", (20, 460), cv2.FONT_HERSHEY_PLAIN, 1,
                        (255, 255, 255), 2)
            cv2.putText(frame, f"Waist Size: {PantSize:.2f}in", (20, 475), cv2.FONT_HERSHEY_PLAIN, 1,
                        (255, 255, 255), 2)

            if ShirtSize <= 16.3:
                cv2.putText(frame, f"S", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            elif ShirtSize <= 17:
                cv2.putText(frame, f"M", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            elif ShirtSize <= 17.8:
                cv2.putText(frame, f"L", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            else:
                cv2.putText(frame, f"XL", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)

            if resetflag == 1:
                MaleFlag = 0
                FemaleFlag = 0
                resetflag = 0
                nextShirt = 0
                nextPant = 0
        elif FemaleFlag == 1:

            shirtFolderPath_female = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\FemaleShirts"
            listShirts = os.listdir(shirtFolderPath_female)
            pantFolderPath_female = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\FemalePants"
            listPants = os.listdir(pantFolderPath_female)

            if fingercount == 1 and nextShirt + 1 < len(listShirts) and not next_shirt_incremented:
                if time.time() - last_increment_time >= delay_duration:
                    nextShirt += 1
                    next_shirt_incremented = True
                    last_increment_time = time.time()
            elif fingercount == 2 :# and not next_shirt_decremented:
                if time.time() - last_decrement_time >= delay_duration:
                    nextShirt -= 1
                    next_shirt_decremented = True
                    last_decrement_time = time.time()

            elif fingercount != 1:
                next_shirt_incremented = False

            elif fingercount != 2:
                next_shirt_decremented = False

            if fingercount == 4 and nextPant + 1 < len(listPants) and not next_pant_incremented:
                if time.time() - last_increment_time >= delay_duration:
                    nextPant += 1
                    next_pant_incremented = True
                    last_increment_time = time.time()

            if fingercount == 5 : #and not next_pant_decremented:
                if time.time() - last_decrement_time >= delay_duration:
                    nextPant -= 1
                    next_pant_decremented = True
                    last_decrement_time = time.time()

            if fingercount != 4:
                next_pant_incremented = False

            if fingercount != 5:
                next_pant_decremented = False

            # Use paths for female shirts and pants
            imgPant = cv2.imread(os.path.join(pantFolderPath_female, listPants[nextPant]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.imread(os.path.join(shirtFolderPath_female, listShirts[nextShirt]), cv2.IMREAD_UNCHANGED)

            imgPant = cv2.resize(imgPant, (widthOfPant, int(2 * widthOfPant * PantRatioHeightWidth)))

            # Pant Offset
            x_offset1 = -50
            y_offset1 = -30

            frame = cvzone.overlayPNG(frame, imgPant, (x_24 + x_offset1, y_24 + y_offset1))

            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(1.05 * widthOfShirt * shirtRatioHeightWidth)))

            # Shirt Offset
            x_offset = -35
            y_offset = -45
            frame = cvzone.overlayPNG(frame, imgShirt, (x_12 + x_offset, y_12 + y_offset))

            # cv2.putText(frame, str(fingercount), (25, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

            # Size Display
            ShirtSize = widthOfShirt * 0.119
            PantSize = widthOfPant * 0.240
            cv2.putText(frame, f"Shoulder Size: {ShirtSize:.2f}in", (20, 460), cv2.FONT_HERSHEY_PLAIN, 1,
                        (255, 255, 255), 2)
            cv2.putText(frame, f"Waist Size: {PantSize:.2f}in", (20, 475), cv2.FONT_HERSHEY_PLAIN, 1,
                        (255, 255, 255), 2)

            if ShirtSize <= 13:
                cv2.putText(frame, f"S", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            elif ShirtSize <= 13.5:
                cv2.putText(frame, f"M", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            elif ShirtSize <= 14:
                cv2.putText(frame, f"L", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)
            else:
                cv2.putText(frame, f"XL", (10, 430), cv2.FONT_HERSHEY_PLAIN, 5.6,
                            (0, 0, 0), 5)

            if resetflag == 1:
                MaleFlag = 0
                FemaleFlag = 0
                resetflag = 0
                nextShirt = 0
                nextPant = 0

        cv2.imshow('Virtual Trial Room', cv2.resize(frame, (1280, 960)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    mp_hands.close()
    mp_pose.close()


if __name__ == "__main__":
    main()
