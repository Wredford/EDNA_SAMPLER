import datetime
import csv
import time

from hardware.led import set_led
from hardware.motors import set_motor

###################### CONFIG ###################################
LOG_FILE = "logs/data.csv"

###################### LOGGING ################################
def log_event(event, motor="", duration=0, notes=""):
    dtnow = datetime.datetime.now()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            dtnow.date(),
            dtnow.time(),
            event,
            motor,
            duration,
            notes
        ])

    print(f"LOG | {event} | motor={motor} | duration={duration}s | {notes}")


###################### MOTOR SEQUENCE ############################

MOTOR_SEQUENCE = [
    ("main1", "pres1"),
    ("main2", "pres2"),
    ("main3", "pres3"),
]


###################### CORE SEQUENCE ENGINE ######################

def run_sequence(sample_duration, pres_duration, interval_min, state=None):

    set_led("sampling")
    log_event("START_SEQUENCE")

    start_time = time.time()

    try:
        for main, pres in MOTOR_SEQUENCE:

            # ---------------- STOP CHECK ----------------
            if state and state.get("stop"):
                log_event("STOP_REQUESTED")
                set_led("off")
                return

            # ---------------- MAIN MOTOR ----------------
            log_event("MAIN_START", motor=main, duration=sample_duration)

            # set_motor(main, True)
            time.sleep(sample_duration)
            # set_motor(main, False)

            log_event("MAIN_STOP", motor=main, duration=sample_duration)

            time.sleep(2)

            # ---------------- STOP CHECK ----------------
            if state and state.get("stop"):
                log_event("STOP_REQUESTED")
                set_led("off")
                return

            # ---------------- PRES MOTOR ----------------
            log_event("PRES_START", motor=pres, duration=pres_duration)

            # set_motor(pres, True)
            time.sleep(pres_duration)
            # set_motor(pres, False)

            log_event("PRES_STOP", motor=pres, duration=pres_duration)

            # ---------------- STOP CHECK ----------------
            if state and state.get("stop"):
                log_event("STOP_REQUESTED")
                set_led("off")
                return

            # ---------------- INTERVAL ----------------
            log_event(
                "INTERVAL_WAIT",
                duration=interval_min * 60,
                notes="Between sample stages"
            )

            time.sleep(interval_min * 60)

    except Exception as e:
        log_event("ERROR", notes=str(e))
        set_led("off")
        raise

    total_time = time.time() - start_time

    log_event("END_SEQUENCE", notes=f"Total runtime: {total_time:.1f} sec")
    set_led("on")


###################### JSON ENTRY POINT ###########################

def run_sampler(config):

    sample_duration = config.get("sample_duration", 10)
    pres_duration = config.get("pres_duration", 5)
    interval = config.get("interval_min", 1)

    run_sequence(sample_duration, pres_duration, interval, state=None)

    config["armed"] = False
    return config


###################### TEST MODE #################################

def run_test(config, state=None):
    """
    Run a single test sampling cycle using the provided configuration.
    """

    sample_duration = config.get("sample_duration", 10)
    pres_duration = config.get("pres_duration", 5)
    interval_min = config.get("interval_min", 1)

    try:
        run_sequence(
            sample_duration=sample_duration,
            pres_duration=pres_duration,
            interval_min=interval_min,
            state=state
        )

    finally:
        # Ensure LED returns to idle even if stopped or interrupted
        set_led("on")


if __name__ == "__main__":
    test_config = {
        "sample_duration": 10,
        "pres_duration": 5,
        "interval_min": 1
    }
    run_test(test_config)