import RPi.GPIO as GPIO
import time
import threading

LED_PIN = 17  # GPIO17 (physical pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

_state = "off"
_blink_thread = None
_stop_blink = False


def _blink_loop():
    global _stop_blink
    while not _stop_blink:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


def set_led(state):
    """
    States:
    - "on"       -> solid ON
    - "off"      -> OFF
    - "sampling" -> blinking
    """

    global _state, _blink_thread, _stop_blink
    _state = state
    print(f"[LED] Setting state: {state}")

    # stop any blinking first
    _stop_blink = True
    if _blink_thread:
        _blink_thread.join()
        _blink_thread = None

    if state == "on":
        time.sleep(2)
        GPIO.output(LED_PIN, GPIO.HIGH)

    elif state == "off":
        time.sleep(2)
        GPIO.output(LED_PIN, GPIO.LOW)

    elif state == "sampling":
        _stop_blink = False
        _blink_thread = threading.Thread(target=_blink_loop, daemon=True)
        _blink_thread.start()

    else:
        print("Unknown LED state:", state)