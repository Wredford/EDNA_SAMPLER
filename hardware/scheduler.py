from datetime import datetime, timedelta


def schedule_wakeup(sample_time):
    """
    Create a one-shot Witty Pi schedule for the next sample event.
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

    schedule_file = "/home/pi/wittypi/schedules/EDNA_SCHEDULE.wpi"

    with open(schedule_file, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Created schedule: {schedule_file}")
    print(f"[Scheduler] Wake at: {target}")