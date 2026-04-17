from flask import Flask, request, jsonify
import json
from sampler import run_test

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
	interval_hours = config.get("interval_hours", 6)
	flow_rate = config.get("flow_rate", 0.5)

	return f"""
	<h1>eDNA Sampler Control Panel</h1>
	<form method="POST" action="/save">
		<label>Sample Duration (sec):</label>
		<input type="number" step=".1" name="sample_duration" value="{sample_duration}"><br><br>

		<label>Interval (hrs):</label>
		<input type="number" step=".01" name="interval_hours" value="{interval_hours}"><br><br>

		<label>Flow Rate (1-10):</label>
		<input type="number" step=".1" min="1" max="10" name="flow_rate" value="{flow_rate}"><br><br>

		<input type="submit" value="Save">
	</form>

	<br>

	<form method="POST" action="/test">
		<input type="submit" value="Test Run">
	</form>
	"""

@app.route("/save", methods=["POST"])
def save():
	data = { "sample_duration": float(request.form["sample_duration"]),
	"interval_hours": float(request.form["interval_hours"]),
	"flow_rate": float(request.form["flow_rate"]) }
	save_config(data)
	return "Saved! <br><a href='/'>Back</a>"

@app.route("/test", methods=["POST"])
def test():
	run_test()
	return "Test Run Started! <br><a href='/'>Back</a>"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
