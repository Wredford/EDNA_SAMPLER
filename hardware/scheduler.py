from datetime import datetime, timedelta
import os

WITTY_PI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTY_PI_DIR}/schedule.wpi"
RUN_SCRIPT = f"{WITTY_PI_DIR}/runScript.sh"

MOTOR_CYCLES = 3

def schedule_wakeup(sample_time, sample_duration, pres_duration, interval_min):

    now = datetime.now()

    # -------- WAKE TIME --------
    wake = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    if wake <= now:
        wake += timedelta(days=1)

    # -------- SIMPLE RUNTIME --------
    runtime_sec = sample_duration + pres_duration + 2
    runtime_min = max(1, int(runtime_sec / 60))

    wake_offset = max(1, int((wake - now).total_seconds() / 60))

    # -------- DEBUG --------
    print("\n========== SCHEDULER DEBUG ==========")
    print(f"Now:        {now}")
    print(f"Wake time:  {wake}")
    print(f"Wake offset (min): {wake_offset}")
    print(f"Runtime (min): {runtime_min}")
    print("=====================================\n")

    # -------- FIXED WITTY PI SCHEDULE --------
    schedule_text = f"""BEGIN {now.strftime('%Y-%m-%d 00:00:00')}
END   2035-12-31 23:59:59

ON M1
OFF M{wake_offset}

ON M{runtime_min}
OFF M1 WAIT
"""

    schedule_file = "/home/ore653/wittypi/schedule.wpi"

    with open(schedule_file, "w") as f:
        f.write(schedule_text)

    # ---------------- APPLY TO WITTY PI ----------------
    os.system(f"cd {WITTY_PI_DIR} && sudo ./runScript.sh")

    print("[Scheduler] Witty Pi schedule applied")
