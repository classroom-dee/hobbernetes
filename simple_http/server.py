import os
import time
import random
import base64
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CACHE_DIR = "/tmp/simple-http"
CACHE_EXPIRY = 600

BASE_URL = "https://picsum.photos/"

target_id = 100

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Track timestamps for cache validity
cache_metadata = {}
stored_items = ["one", "two", "three", "four"]

class MinimalImageServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global target_id
        image_path = os.path.join(CACHE_DIR, f"{target_id}.jpg")
        now = time.time()

        last_fetched = cache_metadata.get(target_id, 0)
        is_expired = (now - last_fetched) > CACHE_EXPIRY
        print(f"Expires in {now - last_fetched}.")
        if not os.path.exists(image_path) or is_expired:
            try:
                # target_id = random.randint(1, 500)
                # Fetch a new image
                url = f'{BASE_URL}{target_id}'
                with urllib.request.urlopen(url) as response:
                    data = response.read()
                    with open(image_path, "wb") as f:
                        f.write(data)
                cache_metadata[target_id] = now
                print(f"[{target_id}] Fetched new image at {time.ctime(now)}")
            except Exception as e:
                self.send_error(500, f"Failed to fetch image: {e}")
                return
        else:
            print(f"[{target_id}] Served from cache")

        # Serve the image
        try:
            with open(image_path, "rb") as f:
                content = f.read()
                img_base64 = base64.b64encode(content).decode("utf-8")

            todos_html = "".join(f"<li>{item}</li>" for item in stored_items)
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Image Viewer</title></head>
            <body>
                <h1>The To-Do App</h1>
                <h3>Image ID: {target_id}</h3>
                <img src="data:image/jpeg;base64,{img_base64}" width="400"/><br><br>

                <form method="get">
                    <input type="text" name="item" placeholder="Add a todo">
                    <input type="submit" value="Submit">
                </form>

                <h2>Current to-do list</h2>
                <ul>{todos_html}</ul>
            </body>
            </html>
            """
            html_bytes = html.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
            
        except Exception as e:
            self.send_error(500, f"Failed to read image: {e}")

def run(server_class=ThreadingHTTPServer, handler_class=MinimalImageServer, port=8060):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
