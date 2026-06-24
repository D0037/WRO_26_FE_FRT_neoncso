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


CORNERS = 12 

SPEED = 30 #speed for the 
STEER_CENTER = 15   #the point where the servo is at the middle

HSIGN = 1 #steering to one way, could be -1
STEER_SIGN = 1

KD_HEADING = 1.6
KP_HEADING = 0.3

KP_CENTERING = 0.08



def main():
    global gyro

    GPIO.setmode(GPIO.BCM)
    move.setup()
    tof.setup()
    cam.setup()  
    log.info("Open challange lopásra kész")


    #Seri gomb wait ide

    gyro.reset()

    target = 0.0
    corners = 0
    turn_left = None
    near = False

    while corners < CORNERS:
        tof_right = tof.get_front()
        tof_left = tof.get_left()
        tof_front = tof.get_front()

        err = target - gyro.get()
        #KP_HEADING * err: if the error is bigger, the bigger the steering gets (P component)
        #KD_HEADING: D component
        #gyro.read_gyro()["z"]: current angular velocity, this makes the motor not overcorrect
        s = HSIGN *(KP_HEADING * err - KD_HEADING * Gyro.read_gyro()["z"])
        if tof_left is not None and tof_right is not None:
            s += KP_CENTERING * (tof_left - tof_right)
        move.set_angle(s)
        move.set_speed(SPEED)
    



def cleanup():
    gyro.kill()
    im.kill()
    move.cleanup()





if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()