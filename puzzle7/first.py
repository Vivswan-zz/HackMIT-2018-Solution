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

    a = cv2.subtract(frame, commonFrame)
    b = np.add.reduce(a, axis=2).reshape((a.shape[0], a.shape[1], 1))
    c = np.repeat(np.multiply(np.nan_to_num(np.divide(b, b)), 255), 3, axis=2).astype(np.uint8)

    commonFrame = c
    cv2.imshow('res', commonFrame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    commonFrame = frame

# cv2.imwrite(file_path + ".jpg", commonFrame)

cv2.destroyAllWindows()
cap.release()
