import eventlet

eventlet.monkey_patch()

import os  # noqa: E402

from api_utils import (  # noqa: E402
  emit_and_log_error,
  get_conn,
  get_logger,
  handle_todos_get,
  init_db,
)
from flask import Flask, jsonify, request  # noqa: E402
from flask_cors import CORS  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
from prometheus_client import Counter, start_http_server  # noqa: E402

API_URI = os.environ.get('API_URI', 'Placeholder')
API_PORT = int(os.environ.get('API_PORT', 1234))
REDIS_URL = os.getenv('REDIS_URL', 'redis://')

app = Flask(__name__)
CORS(app)
socketio = SocketIO(
  app,
  cors_allowed_origins='*',
  message_queue=REDIS_URL,
  async_mode='eventlet',
  logger=True,
  engineio_logger=True,
)
log = get_logger()
reqs_count = Counter('todo_post_reqs_count', 'Total number of POST requests to /todo')

with app.app_context():
  init_db()  # but it doesn't need flask at all ... 🤔


@app.get('/')
def health_check():
  return 'ok', 200


@app.get('/ready')
def readiness():
  try:
    with get_conn() as conn, conn.cursor() as cur:
      cur.execute('SELECT 1')
  except Exception as e:
    conn.close()
    return str(e), 500
  conn.close()
  return '', 200


@app.route(API_URI, methods=['GET', 'POST'])
def todos():
  if request.method == 'GET':
    rows = handle_todos_get()
    return jsonify(
      [{'id': row[0], 'item': row[1], 'created_at': row[2]} for row in rows]
    )

  # for POST req
  item = (request.get_json() or {}).get('item')
  if not item:
    emit_and_log_error(item, log, socketio)
    return jsonify({'error': "Missing 'item'"}), 400

  if len(item) > 140:
    emit_and_log_error(item, log, socketio)
    return jsonify({'error': 'Text is too long'}), 400

  with get_conn() as conn, conn.cursor() as cur:
    cur.execute(
      'INSERT INTO todos (item) VALUES (%s) RETURNING id, created_at', (item,)
    )
    inserted_id, created_at = cur.fetchone()
    conn.commit()
  conn.close()

  # broadcast -> redis/socketIO
  socketio.emit(
    'todo_added',
    {'id': inserted_id, 'item': item, 'created_at': created_at.isoformat()},
  )

  reqs_count.inc()

  return jsonify({'message': 'Item added'}), 201


# for "Done"
@app.route(f'{API_URI}/<int:id>', methods=['PUT'])
def update_todo(id):
  # item = (request.get_json() or {}).get('item')

  # if not item:
  #   return jsonify({'error': "Missing 'item'"}), 400

  with get_conn() as conn, conn.cursor() as cur:
    cur.execute('UPDATE todos SET done=%s WHERE id=%s RETURNING id', (True, id))
    if not cur.fetchone():
      return jsonify({'error': 'Not found'}), 404
    conn.commit()
  conn.close()

  socketio.emit('todo_done', {'id': id})

  return jsonify({'message': 'Item updated'})


if __name__ == '__main__':
  start_http_server(8000)  # served at pod:8000
  socketio.run(app, port=API_PORT, host='0.0.0.0', debug=False)
