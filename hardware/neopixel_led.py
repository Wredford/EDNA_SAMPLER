from rpi_ws281x import PixelStrip, Color

LED_COUNT = 1
LED_PIN = 12 #pin 32, has BCM
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL
)

strip.begin()

def set_led(state):
    """
    States:
    - "test"  -> blue
    - "error" -> red
    - "idle"  -> off
    """

    if state == "test":
        color = Color(0, 0, 255)

    elif state == "error":
        color = Color(255, 0, 0)

    elif state == "idle":
        color = Color(0, 0, 0)

    else:
        print("Unknown LED state")
        return

    strip.setPixelColor(0, color)
    strip.show()