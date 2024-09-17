import M5
from M5 import *


def setup():
  M5.begin()
  Widgets.fillScreen(0x000000)

def loop():
  M5.update()
  if BtnA.isPressed():
    Widgets.fillScreen(0xFF0000)
  elif BtnB.isPressed():
    Widgets.fillScreen(0x00FF00)
  else:
    Widgets.fillScreen(0x000000)

if __name__ == "__main__":
  setup()
  
  while True:
    loop()
