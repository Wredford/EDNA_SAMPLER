import datetime
import csv
import time

from hardware.led import set_led
from hardware.motors import set_motor

###################### CONFIG ###################################
LOG_FILE = "logs/data.csv"

###################### LOGGING ################################
def log_event(event, pres_duration=0, sample_duration=0, notes=""):
    dtnow = datetime.datetime.now()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            dtnow.date(),
            dtnow.time(),
            event,
            pres_duration,
            sample_duration,
            notes
        ])

    print(f"LOG: {event}, Preservative Duration={pres_duration}, Sample Duration={sample_duration}, Notes={notes}")


###################### MOTOR SEQUENCE ############################

MOTOR_SEQUENCE = [
    ("main1", "pres1"),
    ("main2", "pres2"),
    ("main3", "pres3"),
]


###################### CORE SEQUENCE ENGINE ######################

def run_sequence(sample_duration, pres_duration, interval):

    set_led("sampling")
    log_event("START_SEQUENCE")

    start_time = time.time()

    try:
        for main, pres in MOTOR_SEQUENCE:

            # ---------------- MAIN MOTOR ----------------
            log_event("MAIN_START", sample_duration=sample_duration, notes=main)

            # set_motor(main, True)   # <-- COMMENTED OUT
            time.sleep(sample_duration)
            # set_motor(main, False)  # <-- COMMENTED OUT

            log_event("MAIN_STOP", sample_duration=sample_duration, notes=main)

            time.sleep(2)

            # ---------------- PRES MOTOR ----------------
            log_event("PRES_START", pres_duration=pres_duration, notes=pres)

            # set_motor(pres, True)   # <-- COMMENTED OUT
            time.sleep(pres_duration)
            # set_motor(pres, False)  # <-- COMMENTED OUT

            log_event("PRES_STOP", pres_duration=pres_duration, notes=pres)

            # ---------------- INTERVAL ----------------
            log_event("INTERVAL_WAIT", sample_duration=interval, notes="Between sample stages")
            time.sleep(interval)

    except Exception as e:
        log_event("ERROR", notes=str(e))
        set_led("off")
        raise

    total_time = time.time() - start_time

    log_event("END_SEQUENCE", notes=f"Total runtime: {total_time:.1f} sec")
    set_led("on")


###################### JSON ENTRY POINT ###########################

def run_sampler(config):
    """
    Runs the full sampling sequence using values loaded from config.json. app
    """

    sample_duration = config.get("sample_duration", 10)
    pres_duration = config.get("pres_duration", 5)
    interval = config.get("interval", 1) * 60  # convert minutes to seconds

    run_sequence(sample_duration, pres_duration, interval)
    config["armed"] = False


###################### TEST MODE #################################

def run_test():
    set_led("sampling")
    run_sequence(sample_duration=10, pres_duration=5, interval=3)
    set_led("on")


if __name__ == "__main__":
    run_test()
