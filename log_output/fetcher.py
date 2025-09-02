import json
import requests
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from helper import load_logs, ping_log, get_pings

class LogsReqHandler(BaseHTTPRequestHandler):
    # def log_request(self, code = "-", size = "-"):
    #     pass
    
    # def log_message(self, format, *args):
    #     pass

    def do_GET(self):
        if self.path in ('/', '/healthz'): # /logs routes here
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        elif self.path == '/all':
            logs = load_logs()
            response = json.dumps(logs, indent=2).encode('utf-8')

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response) # or use byte string for plaintext
        elif self.path == '/ping':
            # ping_count = len(get_pings()) # File-based method
            ping_count = 0
            try:
                resp = requests.get('http://ping-pong-svc/pings')
                data = resp.json() # { count: n }
                ping_count = data.get("count", 0)

                log = ping_log('INFO', f'Counts: {ping_count}')
                response = f'{log}\nPing / Pongs: {ping_count}'

                self.send_response(200)
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error: {e}'.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8088), LogsReqHandler)
    print("Listening on port 8088")
    server.serve_forever()

if __name__ == "__main__":
    run()