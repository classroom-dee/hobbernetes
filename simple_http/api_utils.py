import asyncio
import json
import logging
import os
import sys
import threading

import psycopg2
from nats.aio.client import Client as NATS
from psycogreen.eventlet import patch_psycopg

patch_psycopg()


def get_conn():
  conn = psycopg2.connect(
    # OR fully qualified: simple-http-pg-svc.project.svc.cluster.local
    host='simple-http-pg-svc',
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
                done BOOLEAN DEFAULT FALSE,
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


# NATS
class NatsPublisher:
  def __init__(self, url: str, logger):
    self.url = url
    self.log = logger
    self.loop = asyncio.new_event_loop()
    self.thread = threading.Thread(target=self._run_loop, daemon=True)
    self.nc = None
    self._ready = threading.Event()

  def _run_loop(self):
    asyncio.set_event_loop(self.loop)
    self.loop.create_task(self._connect_forever())
    self._ready.set()
    self.loop.run_forever()

  async def _connect_forever(self):
    # Simple POC: retry forever
    while True:
      try:
        nc = NATS()
        await nc.connect(servers=[self.url])
        self.nc = nc
        self.log.info(f'NATS connected: {self.url}')
        return
      except Exception as e:
        self.log.warning(f'NATS connect failed: {e}. Retrying in 2s...')
        await asyncio.sleep(2)

  def start(self):
    self.thread.start()
    self._ready.wait()

  def publish_json(self, subject: str, obj: dict):
    # Fire-and-forget publish; logs errors but doesn't block the request.
    if not self.nc:
      self.log.warning('NATS not connected yet; skipping publish')
      return

    payload = json.dumps(obj, default=str).encode('utf-8')

    async def _pub():
      if self.nc:
        await self.nc.publish(subject, payload)
      else:
        self.log.warning(f'NATS publish failed subject={subject}')

    try:
      asyncio.run_coroutine_threadsafe(_pub(), self.loop)
    except Exception as e:
      self.log.warning(f'Failed to schedule NATS publish: {e}')
