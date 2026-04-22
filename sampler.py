import datetime
import csv
import time
from individual_sample import run_pump
from hardware.neopixel_led import set_led
# import RPi.GPIO as GPIO

###################### CONFIG ###################################
LOG_FILE = "logs/data.csv"

###################### LOGGING ################################
def log_event(event, flow_rate=0, duration=0, notes=""):
	dtnow = datetime.datetime.now()

	with open(LOG_FILE, "a", newline="") as f:
		writer = csv.writer(f)
		writer.writerow([dtnow.date(), dtnow.time(), event, flow_rate, duration, notes ])
	print(f"LOG: {event}, Flow={flow_rate}, Duration={duration}, Notes={notes}")

##################### HARDWARE ####################################

# UNDO THIS WHEN READY
#GPIO.setmode(GPIO.BCM)
#LED_PIN = 
#BUTTON_PIN = 

#GPIO.setup(LED_PIN, GPIO.OUT)
#GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def read_switch():
	# PUT GPIO PIN HERE
	return False

def read_flow():

	return 2.5 #REPLACE

def set_LED(state):
    set_led(state)

############################# MONITOR FUNCTION ######################




############################# MAIN SAMPLING FUNCTIONS  ###############

def run_test():
    set_LED("test")
    run_sample(5)
    set_LED("idle")

def run_sample(duration):
    set_LED("test")

    try:
        run_pump(duration)

    except Exception as e:
        set_LED("error")
        raise e

if __name__ == "__main__":
	print("Running sampler...")
	run_test()
