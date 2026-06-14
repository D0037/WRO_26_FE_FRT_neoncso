from picamera2 import Picamera2
import utils.stream as stream
import numpy as np
import threading
import time
import cv2
import config
import utils.log as log

latest_frame = None
height, width = 0, 0
picam2 = None
_kill = False

def kill():
    global _kill
    _kill = True
    camera_thread.join()

def hsv_filter(frame, color):
    mask = cv2.inRange(frame, np.array(config.HSV_FILTERS[color]["lower"]), np.array(config.HSV_FILTERS[color]["upper"]))
    return mask

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

def get_blocks():
    hsv = cv2.cvtColor(latest_frame, cv2.COLOR_BGR2HSV)

    # HSV filtering using predefined ranges
    green_mask = hsv_filter(hsv, "green")
    red_mask = hsv_filter(hsv, "red")


    # Noise reduction
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 10))
    cv2.erode(green_mask, kernel, green_mask, iterations=1)
    cv2.erode(red_mask, kernel, red_mask, iterations=1)
    cv2.dilate(green_mask, kernel, green_mask, iterations=1)
    cv2.dilate(red_mask, kernel, red_mask, iterations=1)

    # Get contours of red and green blocks
    red_cnts, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    green_cnts, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    # Filter for countours with an area greater than threshold
    red_cnts = list(filter(lambda c: cv2.contourArea(c) >= config.BLOCK_TRSH, red_cnts))
    green_cnts = list(filter(lambda c: cv2.contourArea(c) >= config.BLOCK_TRSH, green_cnts))

    # Create lists with the coordinates and sizes of the block contours
    red_blocks = [(cnt_middle(cnt), cv2.contourArea(cnt), cnt) for cnt in red_cnts]
    green_blocks = [(cnt_middle(cnt), cv2.contourArea(cnt), cnt) for cnt in green_cnts]

    dbg_frame = latest_frame.copy()
    for m, a, c in red_blocks:
        dbg_frame = cv2.drawContours(dbg_frame, (c,), -1, (0, 0, 255), 5)
        dbg_frame = cv2.circle(dbg_frame, m, 3, (255, 255, 255), -1)
    
    stream.show("pls", dbg_frame)

    return red_blocks, green_blocks


def camera_loop():
    global _kill
    global height, width, latest_frame
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

    while not _kill:
        frame = picam2.capture_array()
        stream.show("test", latest_frame)
        latest_frame = frame.copy()

camera_thread = threading.Thread(target=camera_loop)

def start():
    camera_thread.start()

if __name__ == "__main__":
    start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill()