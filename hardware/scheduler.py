from datetime import datetime, timedelta
import os

WITTY_PI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTY_PI_DIR}/schedule.wpi"
RUN_SCRIPT = f"{WITTY_PI_DIR}/runScript.sh"

MOTOR_CYCLES = 3


def schedule_wakeup(sample_time, sample_duration, pres_duration, interval_min):
    """
    Witty Pi schedule:
    - Wake (ON) at sample_time
    - Run full experiment
    - Force OFF after computed runtime + buffer
    """

    now = datetime.now()

    # ---------------- WAKE TIME ----------------
    wake = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    if wake <= now:
        wake += timedelta(days=1)

    interval_sec = interval_min * 60

    # ---------------- RUNTIME ----------------
    cycle_time = sample_duration + pres_duration + interval_sec + 2
    total_runtime = cycle_time * MOTOR_CYCLES

    shutdown = wake + timedelta(seconds=total_runtime + 120)

    # ---------------- WPI SCHEDULE ----------------
    schedule_text = f"""BEGIN {wake.strftime('%Y-%m-%d %H:%M:%S')}
END   {shutdown.strftime('%Y-%m-%d %H:%M:%S')}

ON    H{wake.strftime('%H')} M{wake.strftime('%M')}
OFF   H{shutdown.strftime('%H')} M{shutdown.strftime('%M')}
"""

    # write active schedule file
    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Wake: {wake}")
    print(f"[Scheduler] Shutdown: {shutdown}")

    # apply to RTC
    os.system(f"sudo {RUN_SCRIPT} {SCHEDULE_FILE}")

    print("[Scheduler] Witty Pi schedule applied")