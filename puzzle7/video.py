import colorsys
import os
import shutil
import cv2
import ffmpeg
import numpy as np

file_path = "puzzle3"
dev_mode = True
# dev_mode = False


alpha = 0.2
lightness = 0.2

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


def set_start(img):
    for i in img:
        for j in i:
            if np.sum(j) > 255:
                j[0] = j[1] = j[2] = 255
            else:
                j[0] = j[1] = j[2] = 0


def remove_alpha(qr):
    return np.maximum(np.divide(np.subtract(qr, (alpha * 255.0)), (1 - alpha)), [0, 0, 0]).astype(np.uint8)


def add_alpha(qr):
    return np.minimum(np.add(np.multiply(qr, (1 - alpha)), (alpha * 255.0)), [255, 255, 255]).astype(np.uint8)


def remove_lightness(qr):
    z = cv2.cvtColor(qr, cv2.COLOR_RGB2HSV_FULL)
    z = np.add(z, np.multiply(z, [0, 0, -lightness]))
    return cv2.cvtColor(z.astype(np.uint8), cv2.COLOR_HSV2RGB_FULL)


def add_lightness(qr):
    z = cv2.cvtColor(qr, cv2.COLOR_RGB2HSV_FULL)
    z = np.add(z, np.multiply(z, [0, 0, +lightness]))
    return cv2.cvtColor(z.astype(np.uint8), cv2.COLOR_HSV2RGB_FULL)


def create_hsv_correctness_mask(incorrect_frame, mask):
    a = cv2.inpaint(incorrect_frame, cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY), 1, cv2.INPAINT_TELEA)
    b = cv2.cvtColor(a, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    c = cv2.cvtColor(incorrect_frame, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    d = np.abs(np.subtract(b, c))
    e = np.max(np.minimum(np.abs(np.subtract(d, 255)), d), axis=2)
    f = e.reshape((a.shape[0], a.shape[1], 1))
    i = np.floor(np.divide(f, 40))
    j = np.repeat(np.multiply(np.nan_to_num(np.divide(i, i)), 255), 3, axis=2).astype(np.uint8)
    k = cv2.subtract(j, cv2.bitwise_not(mask))
    return k


def create_hsv_correctness_filtered(incorrect_qr_frame, non_qr_frame, mask, iteration):
    a = cv2.add(incorrect_qr_frame, non_qr_frame)
    b = create_hsv_correctness_mask(a, mask)
    for i in range(iteration - 1):
        b = create_hsv_correctness_mask(a, b)
    return b


def create_hsv_correctness_filtered_map(incorrect_qr_frame, non_qr_frame, mask, n):
    shift_size = 1
    a = cv2.max(cv2.warpAffine(mask, np.float32([[1, 0, shift_size], [0, 1, 0]]), (mask.shape[1], mask.shape[0])), mask)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, 0], [0, 1, shift_size]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, -shift_size], [0, 1, 0]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, 0], [0, 1, -shift_size]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, shift_size], [0, 1, shift_size]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, shift_size], [0, 1, -shift_size]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, -shift_size], [0, 1, shift_size]]), (a.shape[1], a.shape[0])), a)
    a = cv2.max(cv2.warpAffine(a, np.float32([[1, 0, -shift_size], [0, 1, -shift_size]]), (a.shape[1], a.shape[0])), a)
    a = create_hsv_correctness_filtered(incorrect_qr_frame, non_qr_frame, a, n)
    g = np.sum(a, axis=2)
    m = np.sum(g, axis=1)
    n = np.sum(g, axis=0)

    h = []
    for i in range(m.shape[0]):
        if m[i] != 0:
            h.append(i)
    h = np.array(h)

    w = []
    for i in range(n.shape[0]):
        if n[i] != 0:
            w.append(i)
    w = np.array(w)

    coor = []
    for i in range(h.shape[0]):
        for j in range(w.shape[0]):
            if g[h[i]][w[j]] != 0:
                coor.append([h[i], w[j]])
    return a, np.array(coor)


def reverse_hsv_predicted_colors(color):
    new_color = np.array([[color]], dtype=np.uint8)[0][0]
    arr = []
    for i in reversal_combinations:
        h, s, v = np.divide(new_color, 255)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r += i[0]
        g += i[1]
        b += i[2]
        h1, s1, v1 = colorsys.rgb_to_hsv(r, g, b)
        v2 = v1 / (1 + lightness)
        if 0 < 1 / (1 + lightness) <= v2 <= 1 < v1 < (1 + lightness) and 0 <= h1 <= 1 and 0 <= s1 <= 1:
            arr.append(np.multiply([h1, s1, v2], 255))

    return np.array(arr, dtype=np.uint8)


def min_return(a, l, k):
    z = np.min(a, axis=0)[k]
    r = []
    s = []
    for i in range(a.shape[0]):
        if a[i][k] == z:
            r.append(l[i])
            s.append(a[i])
    return np.array(r, dtype=l.dtype), np.array(s, dtype=a.dtype)


def find_correct_hlv_pixel(hlv_corrected_pixel, cv_predicted_pixel):
    a = hlv_corrected_pixel.astype(np.float32)
    b = cv_predicted_pixel.astype(np.float32)
    c = np.abs(np.subtract(a, b))
    d = np.add(np.multiply(np.minimum(np.abs(np.subtract(c, 255)), c), [1, 0, 0]), np.multiply(c, [0, 1, 1]))
    e, f = min_return(d, a, 0)
    g, h = min_return(f, e, 1)
    i, j = min_return(h, g, 2)
    return i[0].astype(hlv_corrected_pixel.dtype)


def hsv_correctness(incorrect_qr_frame, non_qr_frame, original_frame, img):
    a, coor = create_hsv_correctness_filtered_map(incorrect_qr_frame, non_qr_frame, img, 8)
    return cv2.subtract(a, cv2.bitwise_not(img))


def checkers():
    if not os.path.exists(file_path + '.mp4'):
        return False

    if os.path.exists('temp'):
        os.remove('temp')
    if os.path.exists(file_path + '.out.mp4'):
        os.remove(file_path + '.out.mp4')

    if dev_mode:
        shutil.rmtree("1_frame", ignore_errors=True)
        shutil.rmtree("2_video", ignore_errors=True)
        shutil.rmtree("3_qr", ignore_errors=True)
        shutil.rmtree("4_qr_2", ignore_errors=True)
        shutil.rmtree("5_qr_3", ignore_errors=True)
        shutil.rmtree("6_qr_4", ignore_errors=True)
        shutil.rmtree("7_final", ignore_errors=True)
        shutil.rmtree("8_result", ignore_errors=True)
        if not os.path.exists("1_frame"):
            os.makedirs("1_frame")
        if not os.path.exists("2_video"):
            os.makedirs("2_video")
        if not os.path.exists("3_qr"):
            os.makedirs("3_qr")
        if not os.path.exists("4_qr_2"):
            os.makedirs("4_qr_2")
        if not os.path.exists("5_qr_3"):
            os.makedirs("5_qr_3")
        if not os.path.exists("6_qr_4"):
            os.makedirs("6_qr_4")
        if not os.path.exists("7_final"):
            os.makedirs("7_final")
        if not os.path.exists("8_result"):
            os.makedirs("8_result")
    return True


def load():
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
    img = cv2.imread(file_path + ".jpg", cv2.IMREAD_UNCHANGED)
    set_start(img)
    return img, video, video_stream


def extract_qr_part(frame):
    a = np.sum(frame, axis=2)
    r = np.sum(a, axis=1)
    c = np.sum(a, axis=0)
    start = [0, 0]
    end = [frame.shape[0], frame.shape[1]]

    part = []

    for i in range(r.shape[0]):
        if r[i] != 0:
            end[0] = i
            if start[0] == 0:
                start[0] = i
    for i in range(c.shape[0]):
        if c[i] != 0:
            end[1] = i
            if start[1] == 0:
                start[1] = i
    if start[0] > 2:
        start[0] -= 2
    if start[1] > 2:
        start[1] -= 2
    if end[0] + 2 < c.shape[0] - 1:
        end[0] += 2
    if end[1] + 2 < r.shape[0] - 1:
        end[1] += 2

    for i in range(start[0], end[0] + 1):
        part.append([])
        for j in range(start[1], end[1] + 1):
            part[len(part) - 1].append(frame[i][j])

    return np.array(part, dtype=np.uint8), start, end


def add_qr_part(frame, qr_part, start, end):
    new_frame = np.copy(frame)
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            new_frame[i][j][0] = qr_part[i - start[0]][j - start[1]][0]
            new_frame[i][j][1] = qr_part[i - start[0]][j - start[1]][1]
            new_frame[i][j][2] = qr_part[i - start[0]][j - start[1]][2]
    return new_frame


def edit(img, inverse_img, video):
    count = 0
    new_video = []
    for frame in video:
        nonQRFrame = cv2.subtract(frame, img)
        QRFrame = cv2.subtract(frame, inverse_img)
        QRFrame2 = remove_alpha(QRFrame)
        QRFrame3 = remove_lightness(QRFrame2)
        QRFrame4 = hsv_correctness(QRFrame3, nonQRFrame, frame, img)
        finalFrame = cv2.add(nonQRFrame, QRFrame4)

        if dev_mode:
            cv2.imwrite("1_frame/frame%d.png" % count, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            cv2.imwrite("3_qr/frame%d.png" % count, cv2.cvtColor(cv2.add(QRFrame, nonQRFrame), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            cv2.imwrite("4_qr_2/frame%d.png" % count, cv2.cvtColor(cv2.add(QRFrame2, nonQRFrame), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            cv2.imwrite("5_qr_3/frame%d.png" % count, cv2.cvtColor(cv2.add(QRFrame3, nonQRFrame), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            cv2.imwrite("6_qr_4/frame%d.png" % count, cv2.cvtColor(cv2.add(QRFrame4, nonQRFrame), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])
            cv2.imwrite("7_final/frame%d.png" % count, cv2.cvtColor(finalFrame, cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_PNG_COMPRESSION, 0])

        cv2.imshow('QRFrame4', cv2.cvtColor(cv2.add(QRFrame4, nonQRFrame), cv2.COLOR_RGB2BGR))
        new_video.append(finalFrame)

        print("Processing: " + str(round((count / video.shape[0]) * 100, 2)) + "%")
        count += 1
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    return new_video


def write(new_video, video_stream):
    f = open('temp', 'wb')
    f.write(np.array(new_video, dtype=np.uint8).tobytes())
    f.close()
    (
        ffmpeg
            .input('temp',
                   format='rawvideo',
                   pix_fmt='rgb24',
                   s=str(video_stream["width"]) + 'x' + str(video_stream["height"]),
                   r=str(round(int(video_stream["nb_frames"]) / float(video_stream['duration']), 2)))
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
        while 1:
            _, frame = cap.read()
            if frame is None:
                break
            cv2.imwrite("8_result/frame%d.png" % count, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            print("Verifying: " + str(round((count / int(video_stream["nb_frames"])) * 100, 2)) + "%")
            count += 1
        cap.release()


def main():
    if not checkers():
        return

    img, video, video_stream = load()
    new_video = edit(img, cv2.bitwise_not(img), video)
    # write(new_video, video_stream)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
