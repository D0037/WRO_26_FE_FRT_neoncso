import RPi.GPIO as GPIO
import config as conf
import qwiic_vl53l1x
import time
import threading
import utils.log as log

"""
Distance mode Max. distance in the dark (cm) Max. distance under strong ambient light (cm)
Short 136 135
Medium 290 76
Long 360 73
"""

_DEFAULT_ADDR = 0x29

SENSORS = [
    {"name": "front", "shut": conf.TOF_SHUT_1, "addr": 0x2a, "roi": (16, 8),  "center": 195, "mode": 2},
    {"name": "right",  "shut": conf.TOF_SHUT_2, "addr": 0x2b, "roi": (16, 4), "center": 199, "mode": 1},
    {"name": "left",  "shut": conf.TOF_SHUT_3, "addr": 0x2c, "roi": (4, 16), "center": 195, "mode": 1},
]

ms_per_measure = conf.MS_PER_MEASURE
measure_density = conf.MEASURE_DENSITY
_POLL_PERIOD = conf.POLL_PERIOD

_lock = threading.Lock()
_dist = {s["name"]: None for s in SENSORS}   
_sensors = {}                                
_kill = False
_thread = None


def _setup_gpio():
    for s in SENSORS:
        GPIO.setup(s["shut"], GPIO.OUT)
        GPIO.output(s["shut"], GPIO.LOW)
    time.sleep(0.05)
 
def _bring_up_sensors():
    for s in SENSORS:
        name = s["name"]

        GPIO.output(s["shut"], GPIO.HIGH)
        time.sleep(0.05)

        dev = qwiic_vl53l1x.QwiicVL53L1X()
        status = dev.init_sensor(0x29)
        log.debug(status)
        if status == 0:
            raise IOError(
                f"TOF '{name}' inicializálás közben elment lopni (status {status}) "
                f"XSHUT pin {s['shut']}"
            )
        dev.set_i2c_address(s["addr"])
        dev.set_distance_mode(s["mode"])
        dev.set_timing_budget_in_ms(ms_per_measure)
        dev.set_inter_measurement_in_ms(measure_density)
        dev.set_roi(s["roi"][0], s["roi"][1], s["center"])
        dev.start_ranging()

        _sensors[name] = dev
        log.info(f"ToF '{name}' ready at 0x{s['addr']:02x}")
        time.sleep(0.05)

def _poll_loop():
    while not _kill:
        for name, dev in _sensors.items():
            try:
                if dev.check_for_data_ready():
                    d = dev.get_distance()
                    valid = dev.get_range_status() == 0  # 0 = no error
                    dev.clear_interrupt()  # arm the next data-ready event
                    if valid:
                        with _lock:
                            _dist[name] = d
            except OSError as e:
                log.warn(f"ToF '{name}' read error: {e}")
        time.sleep(_POLL_PERIOD)
def setup():
    global _kill, _thread
    
    kill = False
 
    _setup_gpio()
    _bring_up_sensors()
 
    _thread = threading.Thread(target=_poll_loop, daemon=True)
    _thread.start()

def get(name):
    with _lock:
        return _dist[name]

def get_front():
    return get("front")

def get_left():
    return get("left")

def get_right():
    return get("right")

def all():
    """Snapshot of all sensors as a {name: mm} dict."""
    with _lock:
        return dict(_dist)

def kill():
    global _kill
    _kill = True
    if _thread is not None:
        _thread.join(timeout=1.0)
    for name, dev in _sensors.items():
        try:
            dev.stop_ranging()
        except OSError:
            pass
    for s in SENSORS:
        GPIO.output(s["shut"], GPIO.LOW)
 

if __name__ == "__main__":
    setup()
    try:
        while True:
            d = all()
            print(f"front: {d['front']}\tleft: {d['left']}\tright: {d['right']}    ", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        kill()
        GPIO.cleanup()