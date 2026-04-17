import time

def run_pump(duration):
	print(f"Pump ON for {duration} seconds")
	time.sleep(duration)
	print("Pump OFF")
