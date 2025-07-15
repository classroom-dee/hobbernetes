import os
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CACHE_DIR = "/tmp/simple-http"
CACHE_EXPIRY = 600
BASE_URL = "https://picsum.photos/500"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Track timestamps for cache validity
cache_metadata = {}

class MinimalImageServer(BaseHTTPRequestHandler):
    def do_GET(self):
        image_id = self.path.strip("/")

        if not image_id.isdigit():
            self.send_error(404, "Invalid image ID")
            return

        image_path = os.path.join(CACHE_DIR, f"{image_id}.jpg")
        now = time.time()

        last_fetched = cache_metadata.get(image_id, 0)
        is_expired = (now - last_fetched) > CACHE_EXPIRY

        if not os.path.exists(image_path) or is_expired:
            try:
                # Fetch a new image
                with urllib.request.urlopen(BASE_URL) as response:
                    data = response.read()
                    with open(image_path, "wb") as f:
                        f.write(data)
                cache_metadata[image_id] = now
                print(f"[{image_id}] Fetched new image at {time.ctime(now)}")
            except Exception as e:
                self.send_error(500, f"Failed to fetch image: {e}")
                return
        else:
            print(f"[{image_id}] Served from cache")

        # Serve the image
        try:
            with open(image_path, "rb") as f:
                content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Failed to read image: {e}")

def run(server_class=ThreadingHTTPServer, handler_class=MinimalImageServer, port=8060):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
