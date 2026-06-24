import math

LOG_PATH = "./logs"
LOG_LEVEL = "DEBUG"

GYRO_ADDR = 0x69

TOF_SHUT_1 = 17
TOF_SHUT_2 = 27
TOF_SHUT_3 = 22

MS_PER_MEASURE = 50
MEASURE_DENSITY = 55
POLL_PERIOD = 0.005

M_PWM_1 = 24
M_PWM_2 = 23

M_ENC_A = 8
M_ENC_B = 7
M_ENC_FACTOR = (42 * math.pi) / 3

BTN_1 = 5
BTN_2 = 6

LED_R = 19
LED_G = 26


HSV_FILTERS = {
    "orange":  {
        "lower": [2, 41, 129],
        "upper": [13, 255, 255],
    },
    "red": {
        "lower": [172, 138, 56],
        "upper": [179, 255, 255],
    },
    "blue": {
        "lower": [110, 52, 55],
        "upper": [130, 255, 255]
    },
    "green": {"lower": [  0, 20,  50], "upper": [ 10, 255, 255]},
    "magenta":{"lower": [150, 10,  10], "upper": [179, 255, 255]},
}

BLOCK_TRSH = 30