from picamera2 import Picamera2
import utils.stream as stream
import numpy as np
import threading
import time
import cv2
import config
import utils.log as log

height, width = 0, 0
picam2 = None
_kill = False

def kill():
    global _kill
    _kill = True
    image_thread.join()

def init():
    global height, width, picam2
    picam2 = Picamera2()
    picam2.start_preview(None)

    picam2.configure(picam2.create_video_configuration(
        main={"format": "RGB888", "size": (1536, 864)} # Lowest resolution, highest framerate
    ))
    picam2.set_controls({"AfMode": 2, "AeEnable": True, "FrameRate": 60}) # Set autofocus mode to continuous and enable auto exposure

    picam2.start()
    stream.init()              # Initialize network-based stream for debugging

    frame = picam2.capture_array()

    height, width, _ = frame.shape  # Get frame dimensions

def cnt_middle(cnt):
    """Calculate the centroid of a contour."""
    M = cv2.moments(cnt)
    if M["m00"] != 0:  # To avoid division by zero
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    return cx, cy

def area_filter(mask, size_coefficient, min_num, max_num):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(cnts) < 1:
        return None, None
    
    # Filter contours based on size keep the biggest n
    # where n is dependent of the largest countour
    # This is useful to remove noise, but if barely anything can be seen, that won't be filtered
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnts = cnts[:min(max_num, round(size_coefficient / max(cv2.contourArea(cnts[0]), 1)) + min_num)]
    
    # set every pixel to black
    mask[:, :] = 0

    # Draw the filtered contours on the mask
    cv2.drawContours(mask, cnts, -1, 255, -1)
    return mask, cnts

def block_mid(hsv):
    green_mask = cv2.inRange(hsv, config.HSV_FILTERS["green"]["lower"], config.HSV_FILTERS["green"]["higher"])
    orange_mask = cv2.inRange(hsv, config.HSV_FILTERS["orange"]["lower"], config.HSV_FILTERS["orange"]["higher"])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 10))
    stream.show("green_raw", green_mask, log.)
    green_mask = cv2.
    

def _i_thread():
    global _kill
    while not _kill:
        frame = picam2.capture_array()
        stream.show("test", frame)

image_thread = threading.Thread(target=_i_thread)

def start():
    image_thread.start()
    

if __name__ == "__main__":
    init()
    start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        kill()