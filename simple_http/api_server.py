import eventlet
eventlet.monkey_patch()
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from api_utils import get_conn

API_URI = os.environ.get("API_URI")
API_PORT = int(os.environ.get("API_PORT"))
REDIS_URL = os.getenv("REDIS_URL", "redis://")

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=REDIS_URL, async_mode="eventlet")

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

@app.route(API_URI, methods=["GET", "POST"])
def handle_todos():
    if request.method == "GET":
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
            rows = cur.fetchall()
            return jsonify([{"id": row[0], "item": row[1], "created_at": row[2]} for row in rows])
    
    # for POST req
    item = (request.get_json() or {}).get("item")
    if not item:
        return jsonify({"error": "Missing 'item'"}), 400

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO todos (item) VALUES (%s) RETURNING id, created_at", (item,))
        inserted_id, created_at = cur.fetchone()
        conn.commit()
    
    # broadcast -> redis/socketIO
    socketio.emit(
        "todo_added",
        {
            "id": inserted_id,
            "item": item,
            "created_at": created_at.isoformat()
        }
    )
    return jsonify({"message": "Item added"}), 201

if __name__ == "__main__":
    socketio.run(app, port=API_PORT, host='0.0.0.0', debug=True)