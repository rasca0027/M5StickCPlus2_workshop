import os, sys, io
import M5
from M5 import *
import time
import uasyncio


label0 = None
rec_data = None
GAIN_FACTOR = 3

async def record_task():
    global rec_data, label0
    while True:
        label0.setText("recording...")
        Mic.begin()
        rec_data = bytearray(8000 * 5)
        Mic.record(rec_data, 8000, False)
        while Mic.isRecording():
            await uasyncio.sleep_ms(100)
        Mic.end()
        Speaker.begin()
        label0.setText("playing...")
        Speaker.playRaw(rec_data, 8000)
        while Speaker.isPlaying():
           time.sleep_ms(500)


async def main():
    uasyncio.create_task(record_task())
    await uasyncio.sleep_ms(500)


def setup():
    global label0
    M5.begin()
    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 30, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    
  

def loop():
    global rec_data
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        uasyncio.run(main())
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
