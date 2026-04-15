import config as conf
import datetime
import os
import config

log_path = ""
log_file = None

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3
log_level = DEBUG

_LEVEL_STR = ["DEBUG", "INFO", "WARN", "ERROR"]


def log(*logs, level=INFO):
    if log_path == "":
        os.system("mkdir -p logs")
        log_path = conf.LOG_PATH + datetime.now().strftime("%y-%m-%d-%H-%M")
        log_file = open(log_path, "a")
        log_level = _LEVEL_STR.index(config.LOG_LEVEL)

    if level >= log_level:
        out_str = ""
        for l in logs:
            out_str += l + ""
        out_str = out_str[:-1]
        out_str = f"{_LEVEL_STR[level]}\t{out_str}\n"
        
        log_file.write(out_str)
        print(out_str, end="")
