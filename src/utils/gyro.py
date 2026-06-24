import time
import smbus2
import threading
import config as conf
import utils.log as log

GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
GYRO_XOUT_H = 0x43
ACCEL_XOUT_H = 0x3B

PWR_MGMT_1 = 0x6B

def read_i16(bus, addr, reg_high):
    # read 2 bytes
    high = bus.read_byte_data(addr, reg_high)
    low = bus.read_byte_data(addr, reg_high + 1)

    # combine
    value = (high << 8) | low

    # unsigned to signed
    if value & 0x8000:
        value -= 0x10000

    return value

class Gyro:
    # fs_sel: 0: 250, 131; 1: 500, 65.5; 2: 1000, 32.8; 3: 2000, 16.4
    def __init__(self, addr = 0x68, fs_sel = 0, afs_sel = 0):
        self.addr = addr

        # calculate scal factors
        self.gyro_scale_factor = 131.0 / (fs_sel + 1)
        self.accel_scale_factor = 16384 / (2 ** afs_sel) 

        # used to kill the gyro process
        self.kill_switch = False

        # used to store current rotation
        self.z = 0.0

        # to prevent drift
        self.offset = 0

        # i2c bus
        self.bus = smbus2.SMBus(1)
        self.bus.write_byte_data(self.addr, PWR_MGMT_1, 0)

        # set scale factor
        current = self.bus.read_byte_data(self.addr, GYRO_CONFIG)
        new_cfg = (current & ~0x18) | (fs_sel << 3)
        self.bus.write_byte_data(self.addr, GYRO_CONFIG, new_cfg)

        current = self.bus.read_byte_data(self.addr, ACCEL_CONFIG)
        new_cfg = (current & ~0x18) | (afs_sel << 3)
        self.bus.write_byte_data(self.addr, ACCEL_CONFIG, new_cfg)

        time.sleep(0.1)
        
        # calibrate to minimize drift
        log.info("Calibrating gyro")
        self.offset = self.calibrate_gyro()
        log.info("Done!")
        log.debug("Gyro offset:", self.offset)

        # spawn gyro process
        self.prev_time = time.time()
        self.gyro_thread = threading.Thread(target=self.gyro_process)
        self.gyro_thread.start()
    
    def reset(self):
        self.z = 0.0

    def get(self):
        return self.z
    
    def gyro_process(self):
        while not self.kill_switch:
            self.time_elapsed = time.time() - self.prev_time
            self.prev_time = time.time()

            # correct values
            z_speed = (read_i16(self.bus, self.addr, GYRO_XOUT_H + 4) / self.gyro_scale_factor) - self.offset

            # update current rotation
            self.z += z_speed * self.time_elapsed

    def calibrate_gyro(self, samples=1000):
        total = 0

        for _ in range(samples):
            val = read_i16(self.bus, self.addr, GYRO_XOUT_H + 4) / self.gyro_scale_factor
            total += val
           # log.debug(val)
            time.sleep(0.01)  # ~100 Hz

        offset = total / samples
        return offset
    
    def kill(self):
        self.kill_switch = True
        self.gyro_thread.join()
    
    
    def read_gyro(self):
        return {
            "x": read_i16(self.bus, self.addr, GYRO_XOUT_H) / self.gyro_scale_factor,
            "y": read_i16(self.bus, self.addr, GYRO_XOUT_H + 2) / self.gyro_scale_factor,
            "z": read_i16(self.bus, self.addr, GYRO_XOUT_H + 4) / self.gyro_scale_factor
        }
    
    def read_accel(self):
        return {
            "x": read_i16(self.bus, self.addr, ACCEL_XOUT_H) / self.accel_scale_factor,
            "y": read_i16(self.bus, self.addr, ACCEL_XOUT_H + 2) / self.accel_scale_factor,
            "z": read_i16(self.bus, self.addr, ACCEL_XOUT_H + 4) / self.accel_scale_factor
        }
    
    def get_ax(self):
        return read_i16(self.bus, self.addr, ACCEL_XOUT_H) / self.accel_scale_factor

    def get_ay(self):
        return read_i16(self.bus, self.addr, ACCEL_XOUT_H + 2) / self.accel_scale_factor

    def get_az(self):
        return read_i16(self.bus, self.addr, ACCEL_XOUT_H + 4) / self.accel_scale_factor