import threading
import config as conf
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
import time

def init():
    GPIO.setmode(GPIO.BCM)

    