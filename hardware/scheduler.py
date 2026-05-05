from datetime import datetime, timedelta
import os

WITTY_PI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTY_PI_DIR}/schedule.wpi"
RUN_SCRIPT = f"{WITTY_PI_DIR}/runScript.sh"

MOTOR_CYCLES = 3


def schedule_wakeup(sample_time, sample_duration, pres_duration, interval_min):

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

    # ---------------- RUNTIME ESTIMATE ----------------
    cycle_time = sample_duration + pres_duration + interval_sec + 2
    total_runtime = cycle_time * MOTOR_CYCLES

    shutdown = wake + timedelta(seconds=total_runtime + 120)

    # ---------------- WPI FILE ----------------
    schedule_text = f"""BEGIN 2026-01-01 00:00:00
END   2035-01-01 23:59:59

OFF M2
ON  H{wake.strftime('%H')} M{wake.strftime('%M')}
OFF M{int(total_runtime / 60) + 2}
"""

    # write file
    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Wake: {wake}")
    print(f"[Scheduler] Shutdown offset: {shutdown}")

    # ---------------- APPLY TO WITTY PI!!!!!!! ----------------                        THIS LINE IS KEY TO THE SCHEDULING WORKING
    os.system(f"cd {WITTY_PI_DIR} && sudo ./runScript.sh")

    print("[Scheduler] Witty Pi schedule applied")