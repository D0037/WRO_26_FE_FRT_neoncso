import time
import config as conf
from utils.gyro import Gyro
import utils.image_proc as im
import utils.log as log
import utils.stream as stream
import cv2

#gyro = Gyro(conf.GYRO_ADDR)
im.start()
time.sleep(1)
try:
   while True:
      im.get_blocks()
except KeyboardInterrupt:
    im.kill()
