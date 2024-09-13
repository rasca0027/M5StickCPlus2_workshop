import os, sys, io
import M5
from M5 import *

is_on = False

def btn_pressed(state):
  global is_on
  is_on = not is_on

def setup():
  M5.begin()
  Widgets.fillScreen(0x000000)
  BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_RELEASED, cb=btn_pressed)
  BtnA.setCallback(type=BtnA.CB_TYPE.WAS_RELEASED, cb=btn_pressed)

def loop():
  M5.update()
  if is_on:
    Widgets.fillScreen(0xFF0000)
  else:
    Widgets.fillScreen(0x000000)

if __name__ == "__main__":
  setup()
  
  while True:
    loop()
