from datetime import datetime, timedelta
import os
import subprocess

WITTYPI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTYPI_DIR}/schedules/EDNA_SCHEDULE.wpi"
RUN_SCRIPT = f"{WITTYPI_DIR}/runScript.sh"


def schedule_wakeup(sample_time):
    """
    Create and apply a one-shot Witty Pi schedule.
    """

    now = datetime.now()

    target = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    if target <= now:
        target += timedelta(days=1)

    end_time = target + timedelta(minutes=15)

    schedule_text = f"""BEGIN {target.strftime('%Y-%m-%d %H:%M:%S')}
END   {end_time.strftime('%Y-%m-%d %H:%M:%S')}
ON    M15
OFF   M1440
"""

    os.makedirs(f"{WITTYPI_DIR}/schedules", exist_ok=True)

    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Created schedule: {SCHEDULE_FILE}")
    print(f"[Scheduler] Wake at: {target}")

    # Apply schedule to Witty Pi
    subprocess.run(
        [RUN_SCRIPT, SCHEDULE_FILE],
        check=True
    )

    print("[Scheduler] Schedule applied to Witty Pi RTC")