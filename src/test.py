import time
import config as conf
from utils.gyro import Gyro
import utils.image_proc as im
import utils.log as log
import utils.stream as stream
import utils.movement as move
import cv2
import RPi.GPIO as GPIO
import utils.tof as tof
import sys

im.start()
GPIO.setmode(GPIO.BCM)
gyro = Gyro(conf.GYRO_ADDR)
move.setup(gyro)

time.sleep(5)

def tof_test():
   csv = open("niga.csv", "a")
   name = sys.argv[1] if len(sys.argv) > 1 else "side"
   tof.setup()
   print(f"{'time(s)':>8}  {'dist(mm)':>9}")
   t0 = time.time()
   try:
      while True:
         dist = tof.get(name)
         #show = "-" if d is None else dist
         log.info(dist)
         csv.write(f"{time.time() - t0},{dist}\n")
   except KeyboardInterrupt:
      pass
   finally:
      csv.close()
      tof.kill()
      GPIO.cleanup()

def image_test():
   while True:
      im.get_direction()
      time.sleep(1/130)

def enc_test():
   move.set_speed(100)
   time.sleep(5)
   move.set_speed(0)
   time.sleep(5)
   move.set_speed(-100)
   time.sleep(5)
   move.set_speed(0)
   move.cleanup()
   exit()
   move.set_speed(0)
   try:
      while True:
         p = move.get_pos()
         log.debug(p)
         
   finally:
      move.cleanup()
   
if __name__ == "__main__":
   try:
      while True:
         log.info(gyro.get(), move.get_pos())
      i#mage_test()
   except KeyboardInterrupt:
      pass
   finally:
      im.kill()
      gyro.kill()
      move.cleanup


try:
   while True:
      pass
      #log.info(move.position)
except KeyboardInterrupt:
   move.cleanup()

