import os
import cv2
import mediapipe as mp
import cvzone

shirtFolderPath = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\Shirts"
listShirts = os.listdir("C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\Shirts")
pantFolderPath = "C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\Pants"
listPants = os.listdir("C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\Pants")
fixedRatio = 154 / 150  # width of shirt / width of points 11 and 12
shirtRatioHeightWidth = 581 / 440
fixedRatio1 = 400 / 150  # width of pant / width of points 23 and 24
PantRatioHeightWidth = 400 / 510
imgButtonRight = cv2.imread("C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\button1.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
imgButtonRight1 = cv2.imread("C:\\Users\\shard\\OneDrive\\Documents\\MEGA\\Mini Project 1B\\Resources-1\\Resources\\button1.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft1 = cv2.flip(imgButtonRight1, 1)


def main():
    counterRight = 0
    counterLeft = 0
    counterRight1 = 0
    counterLeft1 = 0
    selectionSpeed = 10
    imageNumber = 0
    imageNumber1 = 0
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Initialize MediaPipe Pose model
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Pose model
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=2),
            )
            # Extract coordinates of landmarks 11 and 12
            landmark_11 = results.pose_landmarks.landmark[11]
            landmark_12 = results.pose_landmarks.landmark[12]
            # Extract coordinates of landmarks 16 and 15 upper buttons
            landmark_16 = results.pose_landmarks.landmark[16]
            landmark_15 = results.pose_landmarks.landmark[15]
            # Extract coordinates of landmarks 23 and 24
            landmark_23 = results.pose_landmarks.landmark[23]
            landmark_24 = results.pose_landmarks.landmark[24]
            # Extract coordinates of landmarks 28 and 27 upper buttons
            landmark_28 = results.pose_landmarks.landmark[28]
            landmark_27 = results.pose_landmarks.landmark[27]

            # For Shirts Convert normalized coordinates to pixel values
            h, w, c = frame.shape
            x_11, y_11 = int(landmark_11.x * w), int(landmark_11.y * h)
            x_12, y_12 = int(landmark_12.x * w), int(landmark_12.y * h)

            widthOfShirt = int(1.55 * abs(x_11 - x_12) * fixedRatio)
            heightOfShirt = int(widthOfShirt * shirtRatioHeightWidth)
            shoulder_size = (landmark_11.x - landmark_12.x) * 182
            print(landmark_28.y)
            cv2.putText(frame, f"Shoulder Size in cm: {shoulder_size:.2f}", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            # For Pants Convert normalized coordinates to pixel values
            h1, w1, c1 = frame.shape
            x_23, y_23 = int(landmark_23.x * w), int(landmark_23.y * h)
            x_24, y_24 = int(landmark_24.x * w), int(landmark_24.y * h)

            widthOfPant = int(abs(x_23 - x_24) * fixedRatio1)
            heightOfPant = int(widthOfPant * PantRatioHeightWidth)
            waist_size = (landmark_23.x - landmark_24.x) * 182
            # print(landmark_23.y)
            # cv2.putText(frame, f"Shoulder Size in cm: {shoulder_size:.2f}", (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0), 2)

            # Load and resize pant image
            imgPant = cv2.imread(os.path.join(pantFolderPath, listPants[imageNumber1]), cv2.IMREAD_UNCHANGED)
            imgPant = cv2.resize(imgPant, (widthOfPant, int(2 * widthOfPant * PantRatioHeightWidth)))
            # imgShirt = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))

            # Overlay pant image (with offset) onto the frame
            x_offset1 = -150  # -190
            y_offset1 = -20  # -55
            frame = cvzone.overlayPNG(frame, imgPant, (x_23 + x_offset1, y_23 + y_offset1))
            # Overlay button image onto the frame
            frame = cvzone.overlayPNG(frame, imgButtonRight1, (550, 400))
            frame = cvzone.overlayPNG(frame, imgButtonLeft1, (25, 400))

            # Load and resize shirt image
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(1.05 * widthOfShirt * shirtRatioHeightWidth)))
            # imgShirt = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))

            # Overlay shirt image (with offset) onto the frame
            x_offset = -180  # -190
            y_offset = -40  # -55
            frame = cvzone.overlayPNG(frame, imgShirt, (x_11 + x_offset, y_11 + y_offset))
            # Overlay button image onto the frame
            frame = cvzone.overlayPNG(frame, imgButtonRight, (550, 36))
            frame = cvzone.overlayPNG(frame, imgButtonLeft, (25, 36))

            if landmark_16.y < 0.20:
                counterRight += 4
                cv2.ellipse(frame, (55, 65), (25, 25), 0, 0,
                            counterRight * selectionSpeed, (0, 255, 0), 16)
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1
            elif landmark_15.y < 0.20:
                counterLeft += 4
                cv2.ellipse(frame, (580, 65), (25, 25), 0, 0,
                            counterLeft * selectionSpeed, (0, 255, 0), 16)
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1

            else:
                counterRight = 0
                counterLeft = 0

            if landmark_28.y < 0.90:
                counterRight1 += 4
                cv2.ellipse(frame, (55, 430), (25, 25), 0, 0,
                            counterRight1 * selectionSpeed, (0, 255, 0), 16)
                if counterRight1 * selectionSpeed > 360:
                    counterRight1 = 0
                    if imageNumber1 < len(listPants) - 1:
                        imageNumber1 += 1
            elif landmark_27.y < 0.90:
                counterLeft1 += 4
                cv2.ellipse(frame, (580, 430), (25, 25), 0, 0,
                            counterLeft1 * selectionSpeed, (0, 255, 0), 16)
                if counterLeft1 * selectionSpeed > 360:
                    counterLeft1 = 0
                    if imageNumber1 > 0:
                        imageNumber1 -= 1

            else:
                counterRight1 = 0
                counterLeft1 = 0

                # Display the frame
        # cv2.imshow('Virtual Trial Room', frame)
        cv2.imshow('Virtual Trial Room', cv2.resize(frame, (640, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    pose.close()


if __name__ == "__main__":
    main()



