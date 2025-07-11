import os
import json
from datetime import datetime, timezone

# maybe logs can be flushed to other sources later because this will not persist
LOG_FILE = "logs.json"
MNT_PATH = "/tmp/logs"
PATH = os.path.join(MNT_PATH, LOG_FILE)

def load_logs():
    if os.path.exists(PATH):
        with open(PATH, 'r') as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(PATH, 'w') as f:
        json.dump(logs, f, indent=2)

def current_timestamp():
    now = datetime.now(timezone.utc)
    return now.isoformat(timespec="seconds").replace('+00:00', 'Z') + "UTC"

def log_event(logs, level, message):
    entry = f"[{current_timestamp()}] [{level}] {message}"
    logs.append(entry)
    save_logs(logs)
    return logs

def load_and_save(log_level, log_message):
    logs = load_logs()
    return log_event(logs, log_level, log_message)