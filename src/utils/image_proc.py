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

def area_filter(mask, size_coefficient, min_num = 1, max_num = 800):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(cnts) < 1:
        return None, []
    
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

def get_direction() -> None | bool:
    hsv = cv2.cvtColor(latest_frame, cv2.COLOR_BGR2HSV)
    orange_mask = hsv_filter(hsv, "orange")
    blue_mask = hsv_filter(hsv, "blue")

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    orange_mask = cv2.erode(orange_mask, kernel)
    orange_mask = cv2.dilate(orange_mask, kernel)

    blue_mask = cv2.erode(blue_mask, kernel)
    blue_mask = cv2.dilate(blue_mask, kernel)

    orange_mask, orange_cnts = area_filter(orange_mask, 70, 3)
    blue_mask, blue_cnts = area_filter(blue_mask, 70, 3)

    dbg_frame = np.zeros(latest_frame.shape, dtype=np.uint8)

    dbg_frame[orange_mask == 255] = (0, 100, 255)
    dbg_frame[blue_mask == 255] += np.array([255, 0, 0], dtype=np.uint8)
    
    #log.debug(orange_cnts, blue_cnts)
    orange_mid = -1
    blue_mid = -1
    try:
        if orange_cnts != None and len(orange_cnts) > 0:
            orange_points = np.vstack(orange_cnts).squeeze()

            if len(orange_points > 1):
                omid_x = int(np.mean(orange_points[:, 0]))
                omid_y = int(np.mean(orange_points[:, 1])) 
                dbg_frame = cv2.circle(dbg_frame, (omid_x, omid_y), 7, (0, 0, 255), -1)
                orange_mid = omid_y

        if blue_cnts != None and len(blue_cnts) > 0:
            blue_points = np.vstack(blue_cnts).squeeze()
            if len(blue_points > 1):
                bmid_x = int(np.mean(blue_points[:, 0]))
                bmid_y = int(np.mean(blue_points[:, 1])) 
                blue_mid = bmid_y

                dbg_frame = cv2.circle(dbg_frame, (bmid_x, bmid_y), 7, (255, 50, 50), -1)
    except:
        pass
    finally:
        if orange_mid > blue_mid:
            log.warn("orange line detected")

            return True
        elif blue_mid > orange_mid:
            log.warn("blue line detected")

            return False

    stream.show("dbg", dbg_frame)


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
    picam2.set_controls({"AfMode": 2, "AeEnable": True, "FrameRate": 50}) # Set autofocus mode to continuous and enable auto exposure

    picam2.start()
    stream.init()              # Initialize network-based stream for debugging

    frame = picam2.capture_array()


    height, width, _ = frame.shape  # Get frame dimensions

    while not _kill:
        frame = picam2.capture_array()
        frame = cv2.rotate(frame, cv2.ROTATE_180) 
        
        # Convert frame to grayscale for black line detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lower_black = np.array([0])
        upper_black = np.array([70])

        # Mask area abovo black walls
        black_mask = cv2.inRange(gray, lower_black, upper_black)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 15)) # Vertical kernel
        black_mask = cv2.dilate(black_mask, kernel, iterations=3) # Dilate to fill gaps and remove noise
        bottom_black_row = black_mask.shape[0] - np.argmax(np.flipud(black_mask), axis=0) - 1 # Find the bottom row of black pixels in each column

        # Set pixels above the bottom black row to black
        for x in range(black_mask.shape[1]):
            frame[:bottom_black_row[x], x] = 0
            
        stream.show("test", frame)
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