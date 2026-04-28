from flask import Flask, request, jsonify, redirect, url_for
import json
from sampler import run_test, run_sampler
import os
import os
from hardware.scheduler import schedule_wakeup
import threading

app = Flask(__name__)

CONFIG = "config.json"

def load_config():
	with open(CONFIG,"r") as f:
		return json.load(f)

def save_config(data):
	with open(CONFIG,"w") as f:
		json.dump(data,f,indent=4)

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

	<form method="POST" action="/test">
		<input type="submit" value="Test Run">
	</form>

	<br>

	<form method="POST" action="/arm">
		<input type="submit" value="Prepare for Next Test">
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

@app.route("/test", methods=["POST"])
def test():

    def background_run():
        run_test()

    thread = threading.Thread(target=background_run)
    thread.start()

    return redirect(url_for("home"))

@app.route("/arm", methods=["POST"])
def arm():
    config = load_config()
    config["armed"] = True
    save_config(config)

    schedule_wakeup(config["sample_time"])
    # os.system("sudo shutdown -h now")

    return "System armed for next scheduled sample.<br><a href='/'>Back</a>"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
