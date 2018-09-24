import colorsys
import os
import shutil
import cv2
import ffmpeg
import numpy as np


if not os.path.exists(file_path + '.mp4'):
    exit(0)

if os.path.exists('temp'):
    os.remove('temp')
if os.path.exists(file_path + '.out.mp4'):
    os.remove(file_path + '.out.mp4')


probe = ffmpeg.probe(file_path + '.mp4')
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
out, _ = (
    ffmpeg
    .input(file_path + '.mp4')
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run(capture_stdout=True)
)
video = (
    np
    .frombuffer(out, np.uint8)
    .reshape([-1, video_stream['height'], video_stream['width'], 3])
)


file_path = "puzzle"
dev_mode = True
img = cv2.imread(file_path + ".jpg", cv2.IMREAD_UNCHANGED)
imprintImg = cv2.imread(file_path + ".jpg", cv2.IMREAD_UNCHANGED)

inverseImg = cv2.bitwise_not(img)


def set_start():
    for i in img:
        for j in i:
            if np.sum(j) > 255:
                j[0] = j[1] = j[2] = 255
            else:
                j[0] = j[1] = j[2] = 0


def remove_alpha(qr):
    return np.maximum(np.subtract(qr, 51), [0, 0, 0]).astype(np.uint8)

count = 0
newVideo = []
set_start()

for frame in video:
    nonQRFrame = cv2.subtract(frame, img)
    QRFrame = cv2.subtract(frame, inverseImg)
    QRFrame2 = remove_alpha(QRFrame)
    finalFrame = cv2.add(QRFrame2, nonQRFrame)

    newVideo.append(finalFrame)

    print("Processing: " + str(round((count / video.shape[0]) * 100, 2)) + "%")
    count += 1

npNewVideo = np.array(newVideo, dtype=np.uint8).tobytes()

f = open('temp', 'wb')
f.write(npNewVideo)
f.close()

(
    ffmpeg
    .input('temp',
           format='rawvideo',
           pix_fmt='rgb24',
           s=str(video_stream["width"]) + 'x' + str(video_stream["height"]),
           r=str(round(video.shape[0] / float(video_stream['duration']), 2)))
    .output(file_path + '.out.mp4',
            pix_fmt=video_stream['pix_fmt'],
            b=video_stream["bit_rate"])
    .run()
)

if os.path.exists('temp'):
    os.remove('temp')

if dev_mode:
    cap = cv2.VideoCapture(file_path + '.out.mp4')
    count = 0
    newVideo = []
    while 1:
        _, frame = cap.read()
        if frame is None:
            break
        cv2.imwrite("8_result/frame%d.jpg" % count, frame)
        print("Verifying: " + str(round((count / video.shape[0]) * 100, 2)) + "%")
        count += 1
    cap.release()

cv2.destroyAllWindows()
