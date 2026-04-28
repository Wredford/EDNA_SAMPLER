import os
from datetime import datetime, timedelta


def schedule_wakeup(sample_time):
    """
    Program Witty Pi to wake up at the next occurrence of sample_time.

    sample_time format: "HH:MM" (24-hour)
    """

    now = datetime.now()

    # Parse desired wake time
    target = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    # If that time has already passed today, schedule for tomorrow
    if target <= now:
        target += timedelta(days=1)

    # Format for Witty Pi schedule script
    wake_time = target.strftime("%H:%M")

    print(f"Scheduling next wake-up for {target}")

    # Create temporary Witty Pi schedule file
    schedule_text = f"""BEGIN 2025-01-01 00:00:00
END   2035-01-01 23:59:59
ON H{wake_time[:2]} M{wake_time[3:]}
OFF M1
"""

    schedule_file = "/home/pi/wittypi/schedules/next_sample.wpi"

    with open(schedule_file, "w") as f:
        f.write(schedule_text)

    # Apply schedule
    os.system(f"sudo /home/pi/wittypi/runScript.sh {schedule_file}")