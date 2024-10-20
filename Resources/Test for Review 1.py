import os
import cv2
import mediapipe as mp
import cvzone

shirtFolderPath = "/home/shardulA2/Desktop/Resources-1/Resources/Shirts"
listShirts = os.listdir("/home/shardulA2/Desktop/Resources-1/Resources/Shirts")
fixedRatio = 154/150  # width of shirt / width of points 11 and 12
shirtRatioHeightWidth = 581/440

def main():
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
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,0,0), thickness=1, circle_radius=2),
            )
            # Extract coordinates of landmarks 11 and 12
            landmark_11 = results.pose_landmarks.landmark[11]
            landmark_12 = results.pose_landmarks.landmark[12]

            # Convert normalized coordinates to pixel values
            h, w, c = frame.shape
            x_11, y_11 = int(landmark_11.x * w), int(landmark_11.y * h)
            x_12, y_12 = int(landmark_12.x * w), int(landmark_12.y * h)

            widthOfShirt = int(1.35*abs(x_11 - x_12) * fixedRatio)
            heightOfShirt = int(widthOfShirt * shirtRatioHeightWidth)
            print((landmark_11.x-landmark_12.x)*165.38)
            #print(landmark_12)

            # Load and resize shirt image
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[0]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(1.25*widthOfShirt * shirtRatioHeightWidth)))
            #imgShirt = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))

            # Overlay shirt image onto the frame
            x_offset = -200
            y_offset = -55
            frame = cvzone.overlayPNG(frame, imgShirt, (x_11+x_offset, y_11+y_offset))

        # Display the frame
        cv2.imshow('Virtual Trial Room', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    main()

