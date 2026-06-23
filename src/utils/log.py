import config as conf
import datetime
import os
import config
import time

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

log_path = ""
log_file = None
start_time = 0
fstring = ["", "", "\033[33m", "\033[31m"]

log_level = DEBUG

_LEVEL_STR = ["DEBUG", "INFO", "WARN", "ERROR"]
def _init():
    global log_file, log_level, start_time
    os.system("mkdir -p logs")
    log_path = f"{conf.LOG_PATH}/kisauto_{datetime.datetime.now().strftime("%y-%m-%d-%H-%M")}.log"
    log_file = open(log_path, "a")
    log_level = _LEVEL_STR.index(config.LOG_LEVEL)
    start_time = time.time()

def debug(*logs):
    if log_file == None:
        _init()
    if log_level <= DEBUG:
        _log(logs, level=DEBUG)

def info(*logs):
    if log_file == None:
        _init()
    if log_level <= INFO:
        _log(logs, level=INFO)

def warn(*logs):
    if log_file == None:
        _init()
    if log_level <= WARN:
        _log(logs, level=WARN)

def error(*logs):
    if log_file == None:
        _init()
    if log_level <= ERROR:
        _log(logs, level=ERROR)

def _log(logs, level=INFO):
    out_str = ""
    for l in logs:
        out_str += str(l) + " "
    out_str = out_str[:-1]
    out_str = f"{(time.time() - start_time): 08.03f}\t{_LEVEL_STR[level]}\t{out_str}\n"
    
    log_file.write(out_str)
    #log_file.flush()
    print(fstring[level] + out_str + "\033[0m", end="")
