import json
import os
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

# maybe logs can be flushed to other sources later because this will not persist
LOG_FILE = "logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
def current_timestamp():
    now = datetime.now(timezone.utc)
    return now.isoformat(timespec="seconds").replace('+00:00', 'Z') + "UTC"

def log_event(logs, level, message):
    entry = f"[{current_timestamp()}] [{level}] {message}"
    logs.append(entry)
    save_logs(logs)

class LogReqHandler(BaseHTTPRequestHandler):
    def log_request(self, code = "-", size = "-"):
        pass
    
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        logs = load_logs()
        # The result address seems to be from Traefik
        log_event(logs, "INFO", f"Received GET request from {hashlib.sha256(self.client_address[0].encode()).hexdigest()}")
        response = json.dumps(logs, indent=2).encode('utf-8')

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)

if __name__ == "__main__":
    logs = load_logs()
    log_event(logs, "INFO", "Server started")

    server = HTTPServer(("0.0.0.0", 8088), LogReqHandler)
    print("Listening on port 8088")
    server.serve_forever()