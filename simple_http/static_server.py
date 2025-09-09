import eventlet

eventlet.monkey_patch()
import os  # noqa: E402

import requests  # noqa: E402
from flask import Flask, Response, jsonify, send_from_directory  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
from static_utils import img_b64  # noqa: E402

# raw = os.environ.get("STATIC_CACHE_DIR")
# print(f"DEBUG STATIC_CACHE_DIR: {repr(raw)}", file=sys.stderr, flush=True)
CACHE_DIR = os.environ.get('STATIC_CACHE_DIR', 'Placeholder')
target_id = int(os.environ.get('STATIC_TARGET_ID', 'Placeholder'))
PORT = int(os.environ.get('STATIC_PORT', 'Placeholder'))
REDIS_URL = os.getenv('REDIS_URL', 'redis://')
API_URL = os.getenv('API_URL', 'Placeholder')
API_URI = os.getenv('API_URI', 'Placeholder')

cache_meta = {}

app = Flask(__name__, static_folder='static')
socketio = SocketIO(
  app, cors_allowed_origins='*', message_queue=REDIS_URL, async_mode='eventlet'
)


@app.route('/')
def index():
  # return Response(html, mimetype="text/html")
  return send_from_directory('static', 'index.html')


@app.route('/image_b64')
def image_b64_route():
  return jsonify({'img': img_b64(cache_meta)})


# technically the url is for the reverse proxy but it's nice to reuse the same value...
@app.route(API_URI, methods=['GET'])
def proxy_todos():
  r = requests.get(f'{API_URL}{API_URI}', timeout=3)
  return Response(r.content, status=r.status_code, mimetype='application/json')


# Incoming websocket traffic from the API
# namespace placeholder
@socketio.on('todo_added')
def handle_remote_add(data):
  # data is already delivered to all clients; no server-side handling needed
  pass


if __name__ == '__main__':
  os.makedirs(CACHE_DIR, exist_ok=True)
  socketio.run(app, port=PORT, host='0.0.0.0', debug=True)
