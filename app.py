from flask import Flask, request, jsonify, redirect, url_for
import json
from sampler import run_test, run_sampler, prime_preservative_pumps
import os
from hardware.scheduler import schedule_wakeup
import threading
from hardware.led import set_led

# May 05 14:51:09 raspberrypi python[2906]: ========== SCHEDULER DEBUG ==========
May 05 14:51:09 raspberrypi python[2906]: Now:        2026-05-05 14:51:09.369284
May 05 14:51:09 raspberrypi python[2906]: Sample time:15:00
May 05 14:51:09 raspberrypi python[2906]: Wake time:  2026-05-05 15:00:00
May 05 14:51:09 raspberrypi python[2906]: Shutdown:   2026-05-05 15:03:21
May 05 14:51:09 raspberrypi python[2906]: Runtime sec:81.0
May 05 14:51:09 raspberrypi python[2906]: Interval s: 0.0
May 05 14:51:09 raspberrypi python[2906]: =====================================
May 05 14:51:09 raspberrypi python[2906]: [Scheduler] Wake: 2026-05-05 15:00:00
May 05 14:51:09 raspberrypi python[2906]: [Scheduler] Shutdown: 2026-05-05 15:03:21
May 05 14:51:09 raspberrypi sudo[2929]:   ore653 : PWD=/home/ore653/wittypi ; USER=root ; COMMAND=./runScript.sh
May 05 14:51:09 raspberrypi sudo[2929]: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)
May 05 14:51:09 raspberrypi python[2930]: --------------- 2026-05-05 14:51:11 ---------------
May 05 14:51:10 raspberrypi python[2930]: Schedule next shutdown at: 2026-05-06 05:52:09
May 05 14:51:10 raspberrypi python[2930]: ---------------------------------------------------
May 05 14:51:10 raspberrypi sudo[2929]: pam_unix(sudo:session): session closed for user root
May 05 14:51:10 raspberrypi python[2906]: [Scheduler] Witty Pi schedule applied
May 05 14:51:10 raspberrypi python[2906]: 172.20.10.5 - - [05/May/2026 14:51:10] "POST /arm HTTP/1.1" 200 -



set_led("on")

app = Flask(__name__)

CONFIG = "config.json"

test_state = {
    "running": False,
    "stop": False
}

def load_config():
    with open(CONFIG, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    config = load_config()

    sample_duration = config.get("sample_duration", 10)
    interval_min = config.get("interval_min", 1)
    pres_duration = config.get("pres_duration", 5.0)
    sample_time = config.get("sample_time", "02:00")

    return f"""
    <h1>eDNA Sampler Control Panel</h1>

    <form method="POST" action="/save">
        <label>Scheduled Sample Time (24-hour HH:MM):</label>
        <input type="time" name="sample_time" value="{sample_time}"><br><br>

        <label>Sample Duration (sec):</label>
        <input type="number" step=".1" name="sample_duration" value="{sample_duration}"><br><br>

        <label>Interval (min):</label>
        <input type="number" step=".01" name="interval_min" value="{interval_min}"><br><br>

        <label>Preservative Pump Runtime (max 20 sec):</label>
        <input type="number" step=".1" max="20" name="pres_duration" value="{pres_duration}"><br><br>

        <input type="submit" value="Save">
    </form>

    <br>

    <form method="POST" action="/prime">
        <input type="submit" value="Prime Preservative Pumps">
    </form>

    <form method="POST" action="/test">
        <input type="submit" value="Full Test Run">
    </form>

    <br>

    <form method="POST" action="/stop">
        <input type="submit" value="Stop Priming/Test">
    </form>

    <br>

    <form method="POST" action="/arm">
        <input type="submit" value="Prepare for Next Deployment">
    </form>
    """


@app.route("/save", methods=["POST"])
def save():
    data = {
        "sample_duration": float(request.form["sample_duration"]),
        "interval_min": float(request.form["interval_min"]),
        "pres_duration": float(request.form["pres_duration"]),
        "sample_time": request.form["sample_time"],
        "armed": False
    }

    save_config(data)
    return "Settings saved!<br><a href='/'>Back</a>"

@app.route("/prime", methods=["POST"])
def prime():

    if test_state["running"]:
        return "Cannot prime while test is running.<br><a href='/'>Back</a>"

    config = load_config()

    def background_run():
        try:
            test_state["running"] = True
            test_state["stop"] = False

            prime_preservative_pumps(config, test_state)

        finally:
            test_state["running"] = False
            test_state["stop"] = False  

    thread = threading.Thread(target=background_run, daemon=True)
    thread.start()

    return redirect(url_for("home"))


@app.route("/test", methods=["POST"])
def test():

    if test_state["running"]:
        return "Already running.<br><a href='/'>Back</a>"

    config = load_config()

    def background_run():
        try:
            test_state["running"] = True
            test_state["stop"] = False

            run_test(config, test_state)

        finally:
            test_state["running"] = False
            test_state["stop"] = False

    thread = threading.Thread(target=background_run, daemon=True)
    thread.start()

    return redirect(url_for("home"))


@app.route("/stop", methods=["POST"])
def stop():
    test_state["stop"] = True
    return redirect(url_for("home"))


@app.route("/arm", methods=["POST"])
def arm():
    config = load_config()
    config["armed"] = True
    save_config(config)

    schedule_wakeup(
        config["sample_time"],
        config["sample_duration"],
        config["pres_duration"],
        config["interval_min"]
    )

    return "System armed for next scheduled sample.<br><a href='/'>Back</a>"


if __name__ == "__main__":
    set_led("on")  # ← initialize LED to idle state
    app.run(host="0.0.0.0", port=5000)
