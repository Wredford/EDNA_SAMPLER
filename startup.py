import json
import datetime
from sampler import run_sampler

CONFIG_FILE = "config.json"


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def parse_sample_time(time_str):
    """Convert HH:MM string to a datetime.time object."""
    return datetime.datetime.strptime(time_str, "%H:%M").time()


def should_run_now(config):
    """Return True if the sampler is armed and it's time to run."""
    if not config.get("armed", False):
        return False

    sample_time = parse_sample_time(config.get("sample_time", "02:00"))
    current_time = datetime.datetime.now().time()

    return current_time >= sample_time


def main():
    config = load_config()

    if should_run_now(config):
        print("Scheduled sample time reached. Starting sampling sequence.")
        run_sampler(config)
    else:
        print("Sampler not armed or scheduled time has not been reached.")


if __name__ == "__main__":
    main()
