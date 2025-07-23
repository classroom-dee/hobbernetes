import os, sys, time, urllib.request
from flask import Flask, Response
import base64

# raw = os.environ.get("STATIC_CACHE_DIR")
# print(f"DEBUG STATIC_CACHE_DIR: {repr(raw)}", file=sys.stderr, flush=True)
CACHE_DIR    = os.environ.get("STATIC_CACHE_DIR")
CACHE_EXPIRY = int(os.environ.get("STATIC_CACHE_EXPIRY"))
BASE_URL     = os.environ.get("STATIC_BASE_URL")
target_id    = int(os.environ.get("STATIC_TARGET_ID"))
PORT         = int(os.environ.get("STATIC_PORT"))
cache_meta   = {}

os.makedirs(CACHE_DIR, exist_ok=True)
app = Flask(__name__)

def img_b64():
    """Returns cached/fresh image as base64."""
    path = os.path.join(CACHE_DIR, f"{target_id}.jpg")
    now  = time.time()
    if not os.path.exists(path) or (now - cache_meta.get(target_id, 0) > CACHE_EXPIRY):
        with urllib.request.urlopen(f"{BASE_URL}{target_id}") as r:
            with open(path, "wb") as f: f.write(r.read())
        cache_meta[target_id] = now

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@app.route("/")
def index():
    """Renders todo list on load, adds todo list and then re-render"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
      <h1>Todo SPA</h1>
      <h3>Image {target_id}</h3>
      <img src="data:image/jpeg;base64,{img_b64()}" width="400"><br><br>

      <form id="todoForm">
        <input id="todoInput" placeholder="Add a todo">
        <button type="submit">Add</button>
      </form>

      <h2>Current list</h2>
      <ul id="list"></ul>

      <script>
        const API = "/todos";

        async function load() {{
          const res  = await fetch(API);
          const data = await res.json();
          document.getElementById('list').innerHTML =
            data.map(t => `<li>${{t}}</li>`).join('');
        }}

        document.getElementById('todoForm').addEventListener('submit', async e => {{
          e.preventDefault();
          const val = document.getElementById('todoInput').value.trim();
          if (!val) return;
          await fetch(API, {{
            method: 'POST',
            headers: {{'Content-Type':'application/json'}},
            body: JSON.stringify({{item: val}})
          }});
          document.getElementById('todoInput').value = "";
          load();
        }});

        window.onload = load;
      </script>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run(port=PORT, host='0.0.0.0', debug=True) # I do this from remote so 0.0.0.0 was necessary.
