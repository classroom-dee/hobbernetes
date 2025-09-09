import json
import logging
import os
import sys

import psycopg2
from psycogreen.eventlet import patch_psycopg

patch_psycopg()


def get_conn():
  conn = psycopg2.connect(
    host='simple-http-pg-svc',  # OR fully qualified: simple-http-pg-svc.project.svc.cluster.local
    port=5432,
    user=os.getenv('POSTGRES_USER', 'Placeholder').strip(),
    password=os.getenv('POSTGRES_PASSWORD', 'Placeholder').strip(),
  )
  return conn


def init_db():
  with get_conn() as conn:
    with conn.cursor() as cur:
      cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                item TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
      conn.commit()


def get_logger():
  sh = logging.StreamHandler(sys.stdout)
  f = logging.Formatter('%(levelname)-8s | %(message)s')
  sh.setFormatter(f)
  log = logging.getLogger('simple-http-logger')
  log.setLevel(logging.INFO)
  log.addHandler(sh)
  return log


def emit_and_log_error(item, log, socketio):
  payload = {
    'endpoint': '/todo',
    'method': 'POST',
    'payload': item,
    'message': "Missing field 'item'",
  }
  log.info(json.dumps({'app': 'simple-http', 'event': 'error', **payload}))
  socketio.emit('error', payload)


# Services
def handle_todos_get():
  with get_conn() as conn, conn.cursor() as cur:
    cur.execute('SELECT * FROM todos ORDER BY created_at DESC')
    return cur.fetchall()
