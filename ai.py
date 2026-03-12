import cv2
import numpy as np

allow_control: bool = False
pixels_per_cm: float = 1.0

def think(frame):
    h, w = frame.shape[:2]

    mask = get_object_mask(frame)

    ys, xs = np.where(mask > 0)
    if len(xs) == 0:
        return None

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    if xmin == 0 or ymin == 0 or xmax >= w - 1 or ymax >= h - 1:
        return None

    object_size = get_object_size(frame, xmin, ymin, xmax)
    object_color = get_object_color(frame, object_size)

    return {
        "size": object_size,
        "color": object_color
    }

def get_object_color(frame, mask):
    object_pixels = frame[mask > 0]
    b, g, r = object_pixels.mean(axis=0)
    return r, g, b

def get_object_size(xmax, xmin, ymax, ymin):
    width_px = xmax - xmin
    height_px = ymax - ymin

    width_cm = width_px / pixels_per_cm
    height_cm = height_px / pixels_per_cm

    return width_cm, height_cm

def get_object_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 | mask2

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    return mask