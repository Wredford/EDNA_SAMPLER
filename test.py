import time
from hardware.neopixel_led import set_led

set_led("test")
time.sleep(2)

set_led("error")
time.sleep(2)

set_led("green")
time.sleep(2)

set_led("idle")