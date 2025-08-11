import os
import psycopg2
import logging
import sys
import json
from flask import jsonify

def get_conn():
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
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
    log = logging.getLogger("simple-http-logger")
    log.setLevel(logging.INFO)
    log.addHandler(sh)
    return log

def emit_and_log_error(item, log, socketio):
    payload = {
        "endpoint": "/todo",
        "method": "POST",
        "payload": item,
        "message": "Missing field 'item'"
    }
    log.info(json.dumps({"app":"simple-http","event":"error", **payload}))
    socketio.emit("error", payload)

# Services
def handle_todos_get():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
        return cur.fetchall()