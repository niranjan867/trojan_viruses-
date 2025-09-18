# harmless_simulator.py
# Purpose: simulate suspicious-like behaviors for testing detection rules.
# SAFE: does NOT perform destructive actions or modify system startup.
# Behaviors simulated:
#  - create a test file in the temp directory
#  - spawn a short-lived child process
#  - attempt a local HTTP GET to 127.0.0.1:8000
#  - write a "would-be-persistence" file (no actual autostart changes)
#  - emit simple log lines to stdout (useful for Sysmon/log collectors)
#
# Usage:
#   1) (Optional) In another terminal run: python -m http.server 8000
#   2) Run: python harmless_simulator.py
#
import os, sys, time, subprocess, tempfile, urllib.request, socket

def create_test_file():
    fn = os.path.join(tempfile.gettempdir(), "simulator_test.txt")
    with open(fn, "a") as f:
        f.write("simulator: test file created at {}\n".format(time.ctime()))
    print("[simulator] Created file:", fn)

def spawn_child_process():
    # spawn a short-lived child process that sleeps for a couple seconds
    print("[simulator] Spawning child process...")
    if sys.platform.startswith("win"):
        # use python to sleep so behavior is consistent across platforms
        subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
    else:
        subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
    print("[simulator] Child process started.")

def local_http_check():
    url = "http://127.0.0.1:8000/"
    print("[simulator] Attempting local HTTP GET to", url)
    try:
        resp = urllib.request.urlopen(url, timeout=3)
        print("[simulator] Local HTTP responded:", resp.status)
    except Exception as e:
        print("[simulator] Local HTTP check failed (expected if no server):", repr(e))

def simulate_persistence_write():
    # Instead of actually creating autostart entries, write a harmless marker file
    fn = os.path.join(tempfile.gettempdir(), "simulator_would_be_persistence.txt")
    with open(fn, "w") as f:
        f.write("This file simulates an attempt to create a persistence/autostart entry.\n")
        f.write("Time: {}\n".format(time.ctime()))
    print("[simulator] Wrote persistence simulation file:", fn)

def emit_logs():
    # Emit some lines that might be interesting to log-based detectors
    print("[simulator][LOG] Event=ProcessStart Parent=unknown Command=harmless_simulator")
    print("[simulator][LOG] Event=NetworkAttempt Dest=127.0.0.1:8000")

def main():
    print("[simulator] Starting harmless simulator.")
    emit_logs()
    create_test_file()
    spawn_child_process()
    local_http_check()
    simulate_persistence_write()
    print("[simulator] Finished.")

if __name__ == "__main__":
    main()
