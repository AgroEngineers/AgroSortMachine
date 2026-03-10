import cv2
import numpy as np

allow_control: bool = False
pixels_per_cm: float

def think(frame):
    h, w = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    if xmin == 0 or ymin == 0 or xmax >= w - 1 or ymax >= h - 1:
        return None

    # размеры
    width_px = xmax - xmin
    height_px = ymax - ymin

    width_cm = width_px / pixels_per_cm
    height_cm = height_px / pixels_per_cm

    # цвет объекта
    object_pixels = frame[mask > 0]
    b, g, r = object_pixels.mean(axis=0)

    rgb = (int(r), int(g), int(b))

    return {
        "width_cm": width_cm,
        "height_cm": height_cm,
        "color_rgb": rgb
    }