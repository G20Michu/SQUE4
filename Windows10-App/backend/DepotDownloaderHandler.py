import subprocess
import threading
from datetime import datetime
import os
import time

def _depot_executable_path():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, "Dependencies", "WindowsX64", "DepotDownloader.exe")


def start_download(login, password, folder, callback=None, log_path="depot_log.txt"):
    cmd = [
        _depot_executable_path(),
        "-username", login,
        "-password", password,
        "-dir", folder,
        "-app", "393380",
        "-depot", "393381",
        "-manifest", "6933829828063991908",
    ]
    log_file = open(log_path, "w", encoding="utf-8")
    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )


    def emit(event, data=None):
        if callback:
            callback(event, data)

    def reader():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                f.seek(0, 2)

                last_line_time = time.time()

                while True:
                    line = f.readline()

                    if line:
                        last_line_time = time.time()  # reset timera

                        line = line.rstrip("\n")
                        lc = line.lower()

                        print("last line:", line)
                        emit("log", line)

                        # --- ERRORS DETECTION ---
                        if (
                                "steam guard" in lc
                                or "enter the code" in lc
                                or "auth code" in lc
                                or "email at" in lc
                        ):
                            emit("steam_guard", line)

                        if "invalid password" in lc:
                            emit("error", "invalid_password")

                        if "ratelimit" in lc:
                            emit("error", "rate_limit")

                        if "initialize steam failed" in lc:
                            emit("error", "init_failed")

                        if "failed to allocate file" in lc:
                            emit("error", "disk_full")

                    # --- PROCESS EXIT ---
                    if process.poll() is not None:
                        code = process.returncode
                        emit("log", f"process_exit_{code}")
                        emit("error" if code != 0 else "log", f"process_exit_{code}")
                        break

                    # --- WATCHDOG (10s brak logów) ---
                    if time.time() - last_line_time > 10:
                        emit("error", "log_timeout_no_output")
                        # możesz NIE kończyć procesu od razu
                        # break  # <- opcjonalnie

                    time.sleep(0.1)

        except Exception as e:
            emit("error", str(e))

        finally:
            log_file.close()

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    return process, t
def send_guard(process, code: str):
    if process and process.stdin:
        process.stdin.write(code + "\n")
        process.stdin.flush()
