import os
import cv2
from cvzone.PoseModule import PoseDetector
import cvzone

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "/home/shardulA2/Desktop/Resources-1/Resources/Shirts"
listShirts = os.listdir("/home/shardulA2/Desktop/Resources-1/Resources/Shirts")
print(listShirts)
fixedRatio = 154/150  # width of shirt/ width of points 11 and 12
shirtRatioHeightWidth = 581/440

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        lm23 = lmList[23][1:3]
        lm24 = lmList[24][1:3]
        widthOfShirt = int((lm11[1] - lm12[1]) * fixedRatio)

        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[0]), cv2.IMREAD_UNCHANGED)
        imgShirt = cv2.resize(imgShirt, (0, 0), None, 0.5, 0.5)

        print(widthOfShirt)

        try:
            # Add both vertical and horizontal offsets
            offset_y = 250  # Vertical offset
            offset_x = 80  # Horizontal offset
            overlay_x = int(lm11[0] - widthOfShirt / 2) + offset_x
            overlay_y = int(lm11[1]) + offset_y

            # Overlay the shirt image with the updated position
            img = cvzone.overlayPNG(img, imgShirt, (overlay_x, overlay_y))

        except:
            pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
