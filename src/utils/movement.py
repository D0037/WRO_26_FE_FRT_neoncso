import RPi.GPIO as GPIO
import time
import config as conf
from rpi_hardware_pwm import HardwarePWM
from utils import log
from utils.gyro import Gyro


gyro = None
servo_pwm: None | HardwarePWM = None
l_pwm: None | GPIO.PWM = None
r_pwm: None | GPIO.PWM = None

position = 0
prev_a = 0
prev_pos = 0
prev_time = time.time()

def encoder_callback(channel):
    global position, last_a
    a = GPIO.input(conf.M_ENC_A)
    b = GPIO.input(conf.M_ENC_B)

    if a != last_a:  # A changed
        if a == b:
            position += 1   # Clockwise
        else:
            position -= 1   # Counter-clockwise
    last_a = a

def setup():
    global servo_pwm, l_pwm, r_pwm, gyro
    GPIO.setup(conf.M_PWM_1, GPIO.OUT)
    GPIO.setup(conf.M_PWM_2, GPIO.OUT)
    GPIO.setup(conf.M_ENC_A, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(conf.M_ENC_B, GPIO.IN, GPIO.PUD_UP)

    GPIO.add_event_detect(conf.M_ENC_A, GPIO.BOTH, callback=encoder_callback)

    servo_pwm = HardwarePWM(pwm_channel=0, hz=50, chip=0)
    servo_pwm.start()

    l_pwm = GPIO.PWM(conf.M_PWM_1, 500)
    r_pwm = GPIO.PWM(conf.M_PWM_2, 500)
    l_pwm.start(0)
    r_pwm.start(0)

    gyro = Gyro()

def set_angle(angle):
    # Map the angle to a duty cycle (0 to 100)
    duty = ((angle + 90) / 36) + 5
    servo_pwm.change_duty_cycle(duty)

def get_pos():
    return position * conf.M_ENC_FACTOR

# Get current speed based on encoder data in cm/s
def get_speed():
    now = time.time()
    dt = now - prev_time
    pos = get_pos()

    speed = (pos - prev_pos) / dt

    prev_pos = pos
    prev_time = now

    return speed


# Set pwm values asccording to desired speed
# if the speed is to be set to 0, it activates break mode
def set_speed(speed: float):
    if speed > 0:
        l_pwm.ChangeDutyCycle(0)
        r_pwm.ChangeDutyCycle(speed)
    elif speed < 0: 
        r_pwm.ChangeDutyCycle(0)
        l_pwm.ChangeDutyCycle(-speed)
    else:
        r_pwm.ChangeDutyCycle(1)
        l_pwm.ChangeDutyCycle(1)



def move(speed, dist, br=False):
    start_pos = get_pos()
    start_angle = gyro.get()
    error_sum = 0
    prev_time = time.time()
    prev_err = 0

    p = 2
    i = 0.1
    d = 0.5

    while get_pos() < start_pos + dist:
        set_speed(speed)
        error = gyro.get() - start_angle

        now = time.time()
        c = error * p
        c += error_sum * i
        c += d * (error - prev_err) / (now - prev_time)

        set_angle(c)

    if br:
        set_speed(0)
        

def cleanup():
    servo_pwm.stop()
    l_pwm.stop()
    r_pwm.stop()
