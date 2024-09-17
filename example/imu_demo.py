"""Uses IMU to change color of the screen."""
import os, sys, io
import M5
from M5 import *
import time
import math


# Constants for unit conversion
SF_G = 1
SF_M_S2 = 9.80665  # 1 g = 9.80665 m/s2 ie. standard gravity
SF_DEG_S = 1
SF_RAD_S = 0.017453292519943  # 1 deg/s is 0.017453292519943 rad/s
ACCCOEF = 0.02
GYROCOEF = 0.98

# global
preInterval = 0
angleX = 0
angleZ = 0
angleY = 0
angleGyroX = 0
angleGyroY = 0
angleGyroZ = 0

def setup():
    global preInterval
    M5.begin()
    Widgets.fillScreen(0x222222)
    preInterval = time.ticks_us()

def loop():
    M5.update()
    x, y, z = get_attitude()
    print(f"x: {x}, y: {y}, z: {x}")  # debug
    r = int((abs(x) % 360) * 255 / 360)
    g = int((abs(y) % 360) * 255 / 360)
    b = int((abs(z) % 360) * 255 / 360)
    Widgets.fillScreen((r << 16) + (g << 8) + b)

def get_attitude() -> tuple:
    global preInterval, angleX, angleY, angleZ, angleGyroX, angleGyroY, angleGyroZ
    # !Attitude angles as yaw, pitch, and roll in degrees.
    accX, accY, accZ = Imu.getAccel() # Get processed acceleration data

    # Compute tilt angles from the accelerometer data
    angleAccX = math.atan2(accY, accZ + abs(accX)) * (SF_DEG_S / SF_RAD_S)  # noqa: N806
    angleAccY = math.atan2(accX, accZ + abs(accY)) * (-SF_DEG_S / SF_RAD_S)  # noqa: N806

    # Get processed gyro data and remove offsets
    gyroX, gyroY, gyroZ = Imu.getGyro()  # noqa: N806

    # Calculate the time elapsed since the last measurement
    interval = (time.ticks_us() - preInterval) / 1000000
    preInterval = time.ticks_us()

    # Compute the change in angles from the gyro data
    angleGyroX += gyroX * interval
    angleGyroY += gyroY * interval
    angleGyroZ += gyroZ * interval

    # Combine accelerometer and gyro angles using complementary filter
    angleX = (GYROCOEF * (angleX + gyroX * interval)) + (
        ACCCOEF * angleAccX
    )
    angleY = (GYROCOEF * (angleY + gyroY * interval)) + (
        ACCCOEF * angleAccY
    )
    angleZ = angleGyroZ  # Z angle is taken from the gyro only

    return tuple([round(angleZ, 3), round(angleAccX, 3), round(angleAccY, 3)])


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
