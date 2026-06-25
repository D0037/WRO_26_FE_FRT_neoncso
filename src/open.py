import time
import config as conf
from utils.gyro import Gyro 
import utils.image_proc as cam
import utils.log as log
import utils.stream as stream
import utils.movement as move
import cv2
import RPi.GPIO as GPIO
from utils import tof

gyro = None

SPEED = 30
MAX_STEER = 45
STEER_SIGN = 1
HSIGN = 1

KP_HEADING = 1.6
KD_HEADING = 0.3
KI_CENTERING = 0.01
I_LIMIT = 20.0

MAX_STRAIGHT_DEGREE = 20 # maximum degree for integrating centering (I component)
FRONT_TOF_CORNER_DISTANCE = 450 
FRONT_CLEAR = 750 #above this limit the corner detection with the front tof reactivates
CORNERS = 12

def turn():
    current_angle = gyro.get()
    target_angle = 0
    if move.turning_direction == "left":
        target_angle = current_angle -90
        move.set_angle(-70)
        while not current_angle <= target_angle:
            move.set_speed(50)
        move.set_speed(0)
    elif move.turning_direction == "right":
        target_angle = current_angle +90
        move.set_angle(70)
        while not current_angle >= target_angle:
            move.set_speed(50)
        move.set_speed(0)
turning_direction = None
def move_until_line(speed, required_count):
    global turning_direction
    
    blue_count = 0
    orange_count = 0

    while orange_count < required_count or blue_count < required_count:

        direction = cam.get_direction()
        if direction == "orange":
            orange_count += 1
        elif direction == "blue":
            blue_count +=1

    if orange_count >= 5:
        turning_direction = "right"
        return True
    elif blue_count >= 5:
        turning_direction = "left"
        return True

    return False

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(conf.BTN_1, GPIO.IN)
    GPIO.wait_for_edge(conf.BTN_1, GPIO.FALLING)

    gyro = Gyro(conf.GYRO_ADDR)
    move.setup(gyro)
    tof.setup()
    cam.setup()
    gyro.reset()

    target = 0.0
    corners = 0

    front = tof.get_front()



    move.move(100, 5, True, move_until_line)
    move.move(50, 100,False)
    turn()
    

    """

    i_center = 0.0

    i_max = I_LIMIT / KI_CENTERING   #clamping the I component at a max value

    prev_t = time.time()


    
    while corners < CORNERS:
        now = time.time()
        dt = now - prev_t
        prev_t = now

        

        tof_right = tof.get_front()
        tof_left = tof.get_left()
        tof_front = tof.get_front()

        err = target - gyro.get()
        rate = gyro.read_gyro()["z"]

        if tof_left is not None and tof_right is not None and abs(err) < MAX_STRAIGHT_DEGREE:
            i_center += (tof_left - tof_right) * dt
            i_center = max(-i_max, min(i_max, i_center))
        
        s = HSIGN * (KP_HEADING * err - KD_HEADING * rate) + KI_CENTERING * i_center
        move.set_angle(max(-MAX_STEER, min(MAX_STEER, s)))
        move.set_speed(SPEED)

        if not near and tof_front is not None and tof_front < FRONT_TOF_CORNER_DISTANCE:
            near = True
            if turn_left is None:
                turn_left = (tof_left or 0)

                target += (90 if turn_left else -90) * HSIGN
                corners +=1
            elif near and (tof_front is None or tof_front >FRONT_CLEAR):
                near = False
            time.sleep(0.01)
        """
def cleanup():
    gyro.kill()
    cam.kill()
    move.cleanup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()

