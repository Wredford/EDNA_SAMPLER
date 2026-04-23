import datetime
import csv
import time

from hardware.led import set_led
from hardware.motors import set_motor

###################### CONFIG ###################################
LOG_FILE = "logs/data.csv"

###################### LOGGING ################################
def log_event(event, pres_time=0, duration=0, notes=""):
    dtnow = datetime.datetime.now()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            dtnow.date(),
            dtnow.time(),
            event,
            pres_time,
            duration,
            notes
        ])

    print(f"LOG: {event}, Flow={pres_time}, Duration={duration}, Notes={notes}")


###################### MOTOR SEQUENCE ############################

MOTOR_SEQUENCE = [
    ("main1", "pres1"),
    ("main2", "pres2"),
    ("main3", "pres3"),
]


###################### CORE SEQUENCE ENGINE ######################

def run_sequence(duration, pres_time, interval):

    set_led("sampling")
    log_event("START_SEQUENCE")

    start_time = time.time()

    try:
        for main, pres in MOTOR_SEQUENCE:

            # ---------------- MAIN MOTOR ----------------
            log_event("MAIN_START", duration=duration, notes=main)

            # set_motor(main, True)   # <-- COMMENTED OUT
            time.sleep(duration)
            # set_motor(main, False)  # <-- COMMENTED OUT

            log_event("MAIN_STOP", duration=duration, notes=main)

            time.sleep(2)

            # ---------------- PRES MOTOR ----------------
            log_event("PRES_START", pres_time=pres_time, notes=pres)

            # set_motor(pres, True)   # <-- COMMENTED OUT
            time.sleep(pres_time)
            # set_motor(pres, False)  # <-- COMMENTED OUT

            log_event("PRES_STOP", pres_time=pres_time, notes=pres)

            # ---------------- INTERVAL ----------------
            log_event("INTERVAL_WAIT", duration=interval)
            time.sleep(interval)

    except Exception as e:
        log_event("ERROR", notes=str(e))
        set_led("off")
        raise

    total_time = time.time() - start_time

    log_event("END_SEQUENCE", duration=total_time)
    set_led("on")


###################### JSON ENTRY POINT ###########################

def run_sampler(config):
    """
    Called directly by your app / Flask endpoint
    """

    duration = config.get("duration", 10)
    pres_time = config.get("pres_time", 5)
    interval = config.get("interval", 3)

    run_sequence(duration, pres_time, interval)


###################### TEST MODE #################################

def run_test():
    set_led("sampling")
    run_sequence(duration=10, pres_time=5, interval=3)
    set_led("on")


if __name__ == "__main__":
    run_test()
