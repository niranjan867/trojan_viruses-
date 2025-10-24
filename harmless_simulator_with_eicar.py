import os
import sys
import time
import subprocess
import tempfile
import urllib.request
import socket
from pathlib import Path

def create_harmless_test_file():
    fn = os.path.join(tempfile.gettempdir(), "simulator_test.txt")
    with open(fn, "a") as f:
        f.write("simulator: test file created at {}\n".format(time.ctime()))
    print(f"[simulator] Created harmless file: {fn}")

def spawn_harmless_child_process():
    print("[simulator] Spawning harmless child process...")
    try:
        if sys.platform.startswith("win"):
            # Use python to sleep so behavior is consistent across platforms
            subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
        else:
            subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"])
        print("[simulator] Harmless child process started.")
    except Exception as e:
        print(f"[simulator] Error spawning child process: {e}")


def local_http_check():
    """Attempts a local HTTP GET request to 127.0.0.1:8000."""
    url = "http://127.0.0.1:8000/"
    print("[simulator] Attempting local HTTP GET to", url)
    try:
        # Set a short timeout to prevent hanging if no server is present
        resp = urllib.request.urlopen(url, timeout=3)
        print("[simulator] Local HTTP responded:", resp.status)
    except urllib.error.URLError as e:
        print(f"[simulator] Local HTTP check failed (expected if no server): {e.reason}")
    except socket.timeout:
        print("[simulator] Local HTTP check timed out (no server response).")
    except Exception as e:
        print(f"[simulator] Local HTTP check failed unexpectedly: {repr(e)}")


def simulate_persistence_write():
    """Writes a harmless marker file to simulate a persistence attempt."""
    fn = os.path.join(tempfile.gettempdir(), "simulator_would_be_persistence.txt")
    with open(fn, "w") as f:
        f.write("This file simulates an attempt to create a persistence/autostart entry.\n")
        f.write("Time: {}\n".format(time.ctime()))
    print(f"[simulator] Wrote persistence simulation file: {fn}")

def emit_logs():
    """Emits simple log lines to stdout for detection rule testing."""
    print("[simulator][LOG] Event=ProcessStart Parent=unknown Command=safe_harmless_simulator")
    print("[simulator][LOG] Event=NetworkAttempt Dest=127.0.0.1:8000")
    print("[simulator][LOG] Event=FileCreate Type=EICAR Location=MultipleUserFolders")


def create_eicar_files_in_common_folders():
    """
    Creates EICAR test files in common user directories like Desktop, Documents,
    Downloads, and Pictures. These files are harmless but trigger antivirus.
    """
    eicar_test_string = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    eicar_filename = "eicar_test_file.txt" # Using .txt to be less intrusive, AV should still detect content

    # Get the user's home directory
    home_dir = Path.home()

    # Define common target directories
    target_dirs = [
        home_dir,
        home_dir / "Desktop",
        home_dir / "Documents",
        home_dir / "Downloads",
        home_dir / "Pictures",
    ]

    print("\n[simulator] Creating EICAR test files in common user folders:")
    for directory in target_dirs:
        # Ensure the directory exists (it should for common folders)
        if directory.is_dir():
            file_path = directory / eicar_filename
            try:
                with open(file_path, "w") as f:
                    f.write(eicar_test_string)
                print(f" - Created '{file_path}'")
            except Exception as e:
                print(f" - Error creating '{file_path}': {e}")
        else:
            print(f" - Directory not found, skipping: {directory}")
    print("[simulator] EICAR file creation complete. Your antivirus should detect these.")


def main():
    print("[simulator] Starting safe and harmless simulator for detection rule testing.")
    emit_logs()

    print("\n--- Simulating Harmless Behaviors ---")
    create_harmless_test_file()
    time.sleep(1)
    spawn_harmless_child_process()
    time.sleep(1)
    local_http_check()
    time.sleep(1)
    simulate_persistence_write()
    time.sleep(1)

    print("\n--- Creating EICAR Test Files ---")
    create_eicar_files_in_common_folders()

    print("\n[simulator] All safe simulations and EICAR file creations complete. No real harm was done.")

if __name__ == "__main__":
    main()