import hashlib
import json
import os
from datetime import UTC, datetime

# maybe logs can be flushed to other sources later because this will not persist
LOG_FILE = 'logs.json'
MNT_PATH = '/tmp/logs'
PATH = os.path.join(MNT_PATH, LOG_FILE)
PING_PATH = os.path.join(MNT_PATH, 'pings.json')


def load_logs():
  if os.path.exists(PATH):
    with open(PATH) as f:
      return json.load(f)
  return []


def save_logs(logs):
  with open(PATH, 'w') as f:
    json.dump(logs, f, indent=2)


def current_timestamp():
  now = datetime.now(UTC)
  return now.isoformat(timespec='seconds').replace('+00:00', 'Z') + 'UTC'


def ping_log(level, greeting: str):
  filepath = '/tmp/config/information.txt'
  try:
    with open(filepath) as f:
      content = f.read().strip()
  except Exception as e:
    print(e)
  env_message = os.getenv('MESSAGE', 'No env defined')
  config_message = f'file content: {content}\nenv variable: MESSAGE={env_message}\n'
  hex_target = hashlib.sha256(greeting.encode('utf-8')).hexdigest()
  ping_message = f'[{current_timestamp()}] [{level}] {hex_target}\n'
  return ping_message + config_message + greeting


def get_pings():
  if os.path.exists(PING_PATH):
    with open(PING_PATH) as f:
      return json.load(f)
  return []


def log_event(logs, level, message):
  entry = f'[{current_timestamp()}] [{level}] {message}'
  logs.append(entry)
  save_logs(logs)
  return logs


def load_and_save(log_level, log_message):
  logs = load_logs()
  return log_event(logs, log_level, log_message)
