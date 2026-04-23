import board
import neopixel

# Single NeoPixel on GPIO10 is NOT needed for this library
# Use a "logical" pin only (Blinka handles mapping internally)

PIXEL_PIN = board.D18   # safe default for Pi NeoPixels
NUM_PIXELS = 1

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    auto_write=True,
    pixel_order=neopixel.GRB
)

def set_led(state):
    """
    States:
    - test  -> blue
    - error -> red
    - green -> green
    - idle  -> off
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