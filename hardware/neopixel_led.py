import board
import neopixel

# 1 LED on GPIO18 (physical pin 12)
pixels = neopixel.NeoPixel(board.D18, 1, auto_write=True)

def set_led(state):
    """
    States:
    - "test"  -> blue
    - "error" -> red
    - "idle"  -> off
    - "green" -> green (optional success state)
    """

    if state == "test":
        color = (0, 0, 255)

    elif state == "error":
        color = (255, 0, 0)

    elif state == "green":
        color = (0, 255, 0)

    elif state == "idle":
        color = (0, 0, 0)

    else:
        print("Unknown LED state:", state)
        return

    pixels[0] = color