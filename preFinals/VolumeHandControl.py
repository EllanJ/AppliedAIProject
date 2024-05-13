import cv2
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm

facecam = cv2.VideoCapture(0)
facecam.set(3, 1280)
facecam.set(4, 720)
detector = htm.handDetector(detectionCon=0.7)

# Setup audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
volBar, volPer = 400, 0
mute_distance_threshold = 20


def toggle_mute(volume, should_mute):
    if volume.GetMute() != should_mute:
        volume.SetMute(should_mute, None)


while True:
    success, img = facecam.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        # Get the status of fingers
        fingers = detector.fingersUp()

        # Filter by the size of detected hand area
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        if 550 < area < 1500:

            # Find distance of index and thumb for volume control
            length, img, lineInfo = detector.findDistance(4, 8, img, lmList)
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            volPer = 10 * round(volPer / 10)  # Smooth volume transition

            # Check if ring finger is down and adjust volume
            if not fingers[2]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (255, 255, 0)
            else:
                colorVol = (255, 0, 0)

        # Mute control based on specific finger contacts
        fContact = True
        for i, j in zip([16, 20], [13, 17]):
            x1, y1 = lmList[i][1], lmList[i][2]
            x2, y2 = lmList[j][1], lmList[j][2]
            if math.hypot(x2 - x1, y2 - y1) > mute_distance_threshold:
                fContact = False
                break
        toggle_mute(volume, fContact)

        # Display updates

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Volume: {int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
        cv2.putText(img, f'Currect Volume: {int(cVol)}%', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("facecam", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
facecam.release()