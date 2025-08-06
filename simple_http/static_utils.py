import os, time, base64
import urllib.request

CACHE_DIR    = os.environ.get("STATIC_CACHE_DIR")
CACHE_EXPIRY = int(os.environ.get("STATIC_CACHE_EXPIRY"))
BASE_URL     = os.environ.get("STATIC_BASE_URL")
target_id    = int(os.environ.get("STATIC_TARGET_ID"))

def img_b64(cache_dic):
    """Returns cached/fresh image as base64."""
    path = os.path.join(CACHE_DIR, f"{target_id}.jpg")
    now  = time.time()
    if not os.path.exists(path) or (now - cache_dic.get(target_id, 0) > CACHE_EXPIRY):
        with urllib.request.urlopen(f"{BASE_URL}{target_id}") as r:
            with open(path, "wb") as f: f.write(r.read())
        cache_dic[target_id] = now

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()