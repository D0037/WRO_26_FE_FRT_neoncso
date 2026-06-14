import math

LOG_PATH = "./logs"
LOG_LEVEL = "DEBUG"

GYRO_ADDR = 0x68

TOF_SHUT_1 = 17
TOF_SHUT_2 = 27
TOF_SHUT_3 = 22

M_PWM_1 = 23
M_PWM_2 = 24

M_ENC_A = 8
M_ENC_B = 7
M_ENC_TPR = 360
M_ENC_FACTOR = (6 * math.pi) / M_ENC_TPR

BTN_1 = 5
BTN_2 = 6

LED_R = 19
LED_G = 26


HSV_FILTERS = {
    "orange":  {"lower": [10,   215,  230], "upper": [ 30, 240, 255]},
    "red": {
        "lower": [172, 138, 56],
        "upper": [179, 255, 255],
    },
    "blue":   {"lower": [90, 200,  255], "upper": [120, 255, 180]},
    "green": {"lower": [  0, 20,  50], "upper": [ 10, 255, 255]},
    "magenta":{"lower": [150, 10,  10], "upper": [179, 255, 255]},
}

BLOCK_TRSH = 30