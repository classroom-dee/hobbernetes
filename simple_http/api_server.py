import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from api_utils import get_conn

API_URI  = os.environ.get("API_URI")
API_PORT = int(os.environ.get("API_PORT"))

app   = Flask(__name__)
CORS(app) # all routes

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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
                rows = cur.fetchall()
                return jsonify([{"id": row[0], "item": row[1], "created_at": row[2]} for row in rows])
    
    # for POST req
    item = (request.get_json() or {}).get("item")
    if not item:
        return jsonify({"error": "Missing 'item'"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO todos (item) VALUES (%s)", (item,))
            conn.commit()

    return jsonify({"message": "Item added"}), 201

if __name__ == "__main__":
    app.run(port=API_PORT, host='0.0.0.0', debug=True)