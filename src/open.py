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

def main():
    global gyro

    GPIO.setmode(GPIO.BCM)
    gyro = Gyro(conf.GYRO_ADDR)
    move.setup()
    tof.setup()
    cam.setup()

    tof_right = tof.get_front()
    tof_left = tof.get_left()
    tof_front = tof.get_front()
    


def cleanup():
    gyro.kill()
    im.kill()
    move.cleanup()





if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
