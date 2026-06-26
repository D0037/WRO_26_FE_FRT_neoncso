import RPi.GPIO as GPIO
import time
import config as conf
from rpi_hardware_pwm import HardwarePWM
from utils import log
from utils.gyro import Gyro
import utils.image_proc as cam
import threading

gyro = None
servo_pwm: None | HardwarePWM = None
l_pwm: None | GPIO.PWM = None
r_pwm: None | GPIO.PWM = None

position = 0
prev_a = 0
prev_pos = 0
prev_time = time.time()

enc_time = time.time()
prev_pos = 0
speed = 0

_kill = False
_speed_thread = None

def encoder_callback_a(channel):
    global position, prev_a, speed, enc_time

    now = time.time()
    a = GPIO.input(conf.M_ENC_A)
    b = GPIO.input(conf.M_ENC_B)

    #log.debug("encoder A")

    if a != prev_a:  # A changed
        if a == b:
            position += 1   # Forward
            speed = conf.M_ENC_FACTOR / (now - enc_time)
        else:
            position -= 1   # Backwards
            speed = -conf.M_ENC_FACTOR / (now - enc_time)
    prev_a = a
    enc_time = now

def speed_thread():
    global speed, prev_pos
    while not _kill:
        if position == prev_pos:
            speed = 0

        prev_pos = position
        time.sleep(0.05)

def setup(g):
    global servo_pwm, l_pwm, r_pwm, gyro, _speed_thread
    GPIO.setup(conf.M_PWM_1, GPIO.OUT)
    GPIO.setup(conf.M_PWM_2, GPIO.OUT)
    GPIO.setup(conf.M_ENC_A, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(conf.M_ENC_B, GPIO.IN, GPIO.PUD_UP)

    GPIO.add_event_detect(conf.M_ENC_A, GPIO.BOTH, callback=encoder_callback_a)

    servo_pwm = HardwarePWM(pwm_channel=0, hz=50, chip=0)
    servo_pwm.start(0)

    l_pwm = GPIO.PWM(conf.M_PWM_1, 200)
    r_pwm = GPIO.PWM(conf.M_PWM_2, 200)
    l_pwm.start(0)
    r_pwm.start(0)

    _speed_thread = threading.Thread(target=speed_thread)
    _speed_thread.start()

    gyro = g

def set_angle(angle):
    # Map the angle to a duty cycle (0 to 100)
    
    duty = min(max(((angle + 12.5) / 36) + 5, 0), 100)
    servo_pwm.change_duty_cycle(duty)

def get_pos():
    return position * conf.M_ENC_FACTOR

# Set pwm values asccording to desired speed
# if the speed is to be set to 0, it activates break mode
def set_speed(speed: float):
    s = max(min(speed, 100), -100)
    if s > 0:
        l_pwm.ChangeDutyCycle(0)
        r_pwm.ChangeDutyCycle(s)
    elif s < 0: 
        r_pwm.ChangeDutyCycle(0)
        l_pwm.ChangeDutyCycle(-s)
    else:
        r_pwm.ChangeDutyCycle(1)
        l_pwm.ChangeDutyCycle(1)



def move(s, dist, br=False, f = None):
    start_pos = get_pos()
    start_angle = gyro.get()
    start_time = time.time()
    error_sum = 0
    prev_time = time.time()
    prev_err = 0

    kp = 5.0
    ki = 0.01
    kd = 0.1

    skp = 0.06
    ski = 0.0007
    skd = 0.001

    s_sum = 0
    s_prev = s
    st_prev = time.time()
    prev_pos = get_pos() - 1

    #set_speed(100)
    #time.sleep(0.1)
    csv = open("niga.csv", "w")
    csv.write("t,pos,error,p,i,d,corr\n")
    
    while get_pos() < start_pos + dist:
        error = gyro.get() - start_angle

        now = time.time()
        p = error * kp
        i = error_sum * ki
        d = -kd * (error - prev_err) / (now - prev_time)
        #log.debug(p, i, d)

        c = p + i + d
        log.debug(f"{get_pos(): 0.2f}\t{error: 0.2f}\t{p: 0.2f}\t{i:0.2f}\t{d: 0.2f}\t{c}")
        csv.write(f"{now - start_time}, {get_pos()},{error},{p},{i},{d},{c}\n")

        ce = 100 
        if prev_pos != get_pos():
            se = s - speed
            sp = se * skp
            si = s_sum * ski
            sd = -skd * (se - s_prev) / (now - st_prev)

            ce = 30 + (sp + si + sd)

            #log.debug(f"{get_pos(): 0.2f}\t{speed: 0.2f}\t{se: 0.2f}\t{sp: 0.2f}\t{si:0.2f}\t{sd: 0.2f}\t{ce}")
            #csv.write(f"{now - start_time}, {get_pos()},{speed},{se},{sp},{si},{sd},{ce}\n")

            s_sum += se
            s_prev = se
            st_prev = now

            set_speed(ce)
            prev_pos = get_pos()

        prev_time = now
        error_sum += error
        prev_err = error

        set_angle(-c + 1)

        if f != None and f():
            break
        
        time.sleep(0.02)

    if br:
        set_speed(0)

def cleanup():
    global _kill
    _kill = True
    _speed_thread.join()
    servo_pwm.stop()
    l_pwm.stop()
    r_pwm.stop()
