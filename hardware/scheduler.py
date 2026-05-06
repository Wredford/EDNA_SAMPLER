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

    # -------- RUNTIME --------
    interval_sec = interval_min * 60
    cycle_time = sample_duration + pres_duration + interval_sec + 2
    total_runtime = cycle_time * MOTOR_CYCLES

    shutdown = wake + timedelta(seconds=total_runtime + 120)

    # -------- FORMAT TIMES --------
    wake_h = wake.strftime("%H")
    wake_m = wake.strftime("%M")

    ########### DISPLAY VALUES FOR JOURNALCTL ###################
    print("\n========== SCHEDULER DEBUG ==========")
    print(f"Now:        {now}")
    print(f"Sample time:{sample_time}")
    print(f"Wake time:  {wake}")
    print(f"Shutdown:   {shutdown}")
    print(f"Runtime sec:{total_runtime}")
    print(f"Interval s: {interval_sec}")
    print("=====================================\n")

    # -------- SCHEDULE --------
    schedule_text = f"""BEGIN {now.strftime('%Y-%m-%d %H:%M:%S')}
END   {shutdown.strftime('%Y-%m-%d %H:%M:%S')}

ON  {wake.strftime('%Y-%m-%d %H:%M:%S')}
OFF {shutdown.strftime('%Y-%m-%d %H:%M:%S')}
"""

    # write file
    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule_text)

    print(f"[Scheduler] Wake: {wake}")
    print(f"[Scheduler] Shutdown: {shutdown}")


    # ---------------- APPLY TO WITTY PI!!!!!!! ----------------                        THIS LINE IS KEY TO THE SCHEDULING WORKING
    os.system(f"cd {WITTY_PI_DIR} && sudo ./runScript.sh")

    print("[Scheduler] Witty Pi schedule applied")