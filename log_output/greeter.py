import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class LogsReqHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path in ('/'):  # healthcheck
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'ok')
    elif self.path == '/message':
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps({'greeting': os.environ.get('MESSAGE', '')}).encode())
    else:
      self.send_response(404)
      self.end_headers()
      self.wfile.write(b'Not found')


def run():
  server = ThreadingHTTPServer(('0.0.0.0', 8088), LogsReqHandler)
  print('Listening on port 8088')
  server.serve_forever()


if __name__ == '__main__':
  run()
