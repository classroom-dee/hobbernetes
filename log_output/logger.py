import hashlib
import time
import signal
import sys
from datetime import datetime
from helper import load_and_save

def handle_exit(sig, frame):
    load_and_save("INFO", f"Logger terminated by {signal.Signals(sig).name}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_exit) # SIGKILL cannot be caught. Cluster sends SIGTERM -> Grace period -> SIGKILL
    signal.signal(signal.SIGINT, handle_exit) # Interrupts
    
    load_and_save("INFO", "Logger started")
    
    while True:
        time.sleep(5)
        load_and_save("INFO", hashlib.sha256(datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()).hexdigest())