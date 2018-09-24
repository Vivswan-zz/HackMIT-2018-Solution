import colorsys
import os
import shutil
import cv2
import ffmpeg
import numpy as np
# from numba import vectorize, cuda

file_path = "puzzle2"
dev_mode = True

if not os.path.exists(file_path + '.mp4'):
    exit(0)

if os.path.exists('temp'):
    os.remove('temp')
if os.path.exists(file_path + '.out.mp4'):
    os.remove(file_path + '.out.mp4')

if not os.path.exists("0_mask"):
    os.makedirs("0_mask")

if dev_mode:
    shutil.rmtree("1_frame", ignore_errors=True)
    shutil.rmtree("2_video", ignore_errors=True)
    shutil.rmtree("3_qr", ignore_errors=True)
    shutil.rmtree("4_qr_2", ignore_errors=True)
    shutil.rmtree("5_final", ignore_errors=True)
    shutil.rmtree("6_result", ignore_errors=True)
    if not os.path.exists("1_frame"):
        os.makedirs("1_frame")
    if not os.path.exists("2_video"):
        os.makedirs("2_video")
    if not os.path.exists("3_qr"):
        os.makedirs("3_qr")
    if not os.path.exists("4_qr_2"):
        os.makedirs("4_qr_2")
    if not os.path.exists("5_final"):
        os.makedirs("5_final")
    if not os.path.exists("6_result"):
        os.makedirs("6_result")

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

img = cv2.imread(file_path + "_box.jpg", cv2.IMREAD_UNCHANGED)

inverseImg = cv2.bitwise_not(img)
alpha = 0.2
lightness = 0.2


def set_start():
    for i in img:
        for j in i:
            if np.sum(j) > 255:
                j[0] = j[1] = j[2] = 255
            else:
                j[0] = j[1] = j[2] = 0


def create_hsv_correctness_mask(QRFrame3, frame, nonQRFrame, img):
    a = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    b = cv2.inpaint(frame, a, 3, cv2.INPAINT_TELEA)
    c = cv2.subtract(b, cv2.bitwise_not(img))
    d = cv2.cvtColor(c, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    e = cv2.cvtColor(cv2.add(QRFrame3, nonQRFrame), cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    f = np.subtract(d, e)
    g = np.multiply(f, [1, 0, 0])
    h = np.abs(g)
    i = np.add.reduce(h, axis=2)
    j = np.minimum(np.abs(np.subtract(i, 255)), i)
    k = j.reshape((b.shape[0], b.shape[1], 1))
    l = np.floor(np.divide(k, 42.5))
    m = np.repeat(np.multiply(np.nan_to_num(np.divide(l, l)), 255), 3, axis=2).astype(np.uint8)
    n = cv2.subtract(m, cv2.bitwise_not(img))
    return n


def create_hsv_correctness_filtered(QRFrame3, frame, nonQRFrame, img, n):
    a = create_hsv_correctness_mask(QRFrame3, frame, nonQRFrame, img)
    for i in range(n - 1):
        a = create_hsv_correctness_mask(QRFrame3, frame, nonQRFrame, a)
    return a


def create_hsv_correctness_filtered_map(QRFrame3, frame, nonQRFrame, img, n):
    a = create_hsv_correctness_filtered(QRFrame3, frame, nonQRFrame, img, n)
    b = np.sum(a, axis=2)
    c = np.sum(b, axis=1)
    d = np.sum(b, axis=0)

    h = []
    for i in range(c.shape[0]):
        if c[i] != 0:
            h.append(i)
    h = np.array(h)

    w = []
    for i in range(d.shape[0]):
        if d[i] != 0:
            w.append(i)
    w = np.array(w)

    coor = []
    for i in range(h.shape[0]):
        for j in range(w.shape[0]):
            if b[h[i]][w[j]] != 0:
                coor.append([h[i], w[j]])
    return a, np.array(coor)


reversal_combinations = [
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]


def reverse_hsv_predicted_colors(color):
    R = []
    for i in reversal_combinations:
        h, s, v = np.divide(color, 255)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r += i[0]
        g += i[1]
        b += i[2]
        h1, s1, v1 = colorsys.rgb_to_hsv(r, g, b)
        v2 = v1 / (1 + lightness)
        if (1 + lightness) > v1 > 1 >= v2 and 0 <= h1 <= 1 and 0 <= s1 <= 1:
            R.append(np.multiply([h1, s1, v2], 255))

    return np.array(R, dtype=np.uint8)


def minReturn(a, l, k):
    z = np.min(a, axis=0)[k]
    r = []
    s = []
    for i in range(a.shape[0]):
        if a[i][k] == z:
            r.append(l[i])
            s.append(a[i])
    return np.array(r, dtype=l.dtype), np.array(s, dtype=a.dtype)


def findCorrectHlvPixel(hlvCorrectedPixel, cvPredictedPixel):
    a = hlvCorrectedPixel.astype(np.float32)
    b = cvPredictedPixel.astype(np.float32)
    c = np.abs(np.subtract(a, b))
    d = np.add(np.multiply(np.minimum(np.abs(np.subtract(c, 255)), c), [1, 0, 0]), np.multiply(c, [0, 1, 1]))
    e, f = minReturn(d, a, 0)
    g, h = minReturn(f, e, 1)
    i, j = minReturn(h, g, 2)
    return i[0].astype(hlvCorrectedPixel.dtype)


def hsv_correctness(QRFrame3, frame, nonQRFrame, img, count):
    a, coor = create_hsv_correctness_filtered_map(QRFrame3, frame, nonQRFrame, img, 5)

    b = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    c = cv2.subtract(cv2.inpaint(cv2.add(QRFrame3, nonQRFrame), b, 5, cv2.INPAINT_TELEA), inverseImg)

    d = cv2.cvtColor(QRFrame3, cv2.COLOR_RGB2HSV_FULL)
    e = cv2.cvtColor(c, cv2.COLOR_RGB2HSV_FULL)
    f = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV_FULL)

    g = []
    for i in coor:
        hlvCorrectedPixel = reverse_hsv_predicted_colors(f[i[0]][i[1]])
        if len(hlvCorrectedPixel) == 0:
            continue

        correctPixel = findCorrectHlvPixel(hlvCorrectedPixel, e[i[0]][i[1]])

        d[i[0]][i[1]][0] = correctPixel[0]
        d[i[0]][i[1]][1] = correctPixel[1]
        d[i[0]][i[1]][2] = correctPixel[2]
        g.append([i[0], i[1], e[i[0]][i[1]], correctPixel])
    print(g)
    return cv2.subtract(QRFrame3, a), a
    # return cv2.cvtColor(d, cv2.COLOR_HSV2RGB_FULL), a


count = 0
newVideo = []
set_start()

for frame in video:
    nonQRFrame = cv2.subtract(frame, img)
    QRFrame = cv2.subtract(frame, inverseImg)
    QRFrame2 = None
    finalFrame = None
    a = frame

    if 1 < count < 17 or 17 < count < 59:
        QRFrame2, a = hsv_correctness(QRFrame, frame, nonQRFrame, img, count)
        finalFrame = cv2.add(QRFrame2, nonQRFrame)
    else:
        QRFrame2 = QRFrame
        finalFrame = frame

    if dev_mode:
        cv2.imwrite("1_frame/frame%d.jpg" % count, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        cv2.imwrite("2_video/frame%d.jpg" % count, cv2.cvtColor(nonQRFrame, cv2.COLOR_RGB2BGR))
        cv2.imwrite("3_qr/frame%d.jpg" % count, cv2.cvtColor(cv2.add(QRFrame, nonQRFrame), cv2.COLOR_RGB2BGR))
        cv2.imwrite("4_qr_2/frame%d.jpg" % count, cv2.cvtColor(cv2.add(QRFrame2, nonQRFrame), cv2.COLOR_RGB2BGR))
        cv2.imwrite("5_final/frame%d.jpg" % count, cv2.cvtColor(finalFrame, cv2.COLOR_RGB2BGR))
        cv2.imwrite("0_mask/frame%d.jpg" % count, cv2.cvtColor(a, cv2.COLOR_RGB2BGR))
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
        cv2.imwrite("6_result/frame%d.jpg" % count, frame)
        print("Verifying: " + str(round((count / video.shape[0]) * 100, 2)) + "%")
        count += 1
    cap.release()

cv2.destroyAllWindows()
