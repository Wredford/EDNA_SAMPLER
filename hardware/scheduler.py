from datetime import datetime, timedelta
import os

WITTY_PI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTY_PI_DIR}/schedule.wpi"
RUN_SCRIPT = f"{WITTY_PI_DIR}/runScript.sh"


def schedule_wakeup(sample_time):
    """
    Create and apply a Witty Pi schedule for next wake event.
    sample_time format: "HH:MM"
    """

    now = datetime.now()

    # build target datetime (today or tomorrow)
    target = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    if target <= now:
        target += timedelta(days=1)

    # give a short active window for sampling (adjust minutes value to be close to your deployment runtime. can base off test run time)
    end_time = target + timedelta(minutes=15)

    schedule_text = f"""BEGIN {target.strftime('%Y-%m-%d %H:%M:%S')}
END   {end_time.strftime('%Y-%m-%d %H:%M:%S')}
ON    M15
OFF   M1440
"""

    # overwrite ACTIVE schedule file (important fix)
    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Wrote schedule to {SCHEDULE_FILE}")
    print(f"[Scheduler] Wake time: {target}")

    # immediately apply schedule to RTC
    cmd = f"sudo {RUN_SCRIPT} {SCHEDULE_FILE}"
    os.system(cmd)

    print("[Scheduler] Schedule applied to Witty Pi RTC")