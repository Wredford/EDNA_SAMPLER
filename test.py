import time
from hardware.led import set_led

print("LED test start")

set_led("on")
time.sleep(2)

set_led("sampling")
time.sleep(6)

set_led("on")
time.sleep(2)

set_led("off")

print("LED test done")