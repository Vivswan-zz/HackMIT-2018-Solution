import os
import cv2
import numpy as np

file_path = "puzzle"
cap = cv2.VideoCapture(file_path + ".mp4")
img = None

_, frame = cap.read()
commonFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

# avg1 = f
# avg0 = f
# if img is None:
#     avg2 = np.float32(f)
# else:
#     avg2 = np.float32(img)

while 1:
    _, frame = cap.read()
    if frame is None:
        break

    a = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])

    mask = cv2.inRange(a, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

cv2.imwrite(file_path + ".jpg", commonFrame)

cv2.destroyAllWindows()
cap.release()
