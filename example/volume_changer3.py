"""Uses IMU to change color of the screen."""
import os, sys, io
import M5
from M5 import *
import time


def setup():
    M5.begin()
    Widgets.fillScreen(0x222222)

def loop():
    M5.update()
    x = min(abs(int((Imu.getAttitude()[0] + 180) * 255 / 360)), 255)
    y = min(abs(int((Imu.getAttitude()[1] + 180) * 255 / 360)), 255)
    z = min(abs(int((Imu.getAttitude()[2] + 180) * 255 / 360)), 255)
    # print(f"x: {x}, y: {y}, z: {x}")
    Widgets.fillScreen((x << 16) + (y << 8) + z)
    # print(hex((x << 16) + (y << 8) + z))
    

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
