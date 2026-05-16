import subprocess
import threading
import os
import time
import re
import win32com.client
import sys
def _depot_executable_path():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, "Dependencies", "WindowsX64", "DepotDownloader.exe")

def create_shortcut_from_folder(folder_path, exe_name=None):
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")

    target_exe = None

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".exe"):
                if exe_name:
                    if file.lower() == exe_name.lower():
                        target_exe = os.path.join(root, file)
                        break
                else:
                    target_exe = os.path.join(root, file)
                    break
        if target_exe:
            break

    if not target_exe:
        print("❌ No EXE found!")
        return

    shortcut_name = os.path.splitext(os.path.basename(target_exe))[0] + ".lnk"
    shortcut_path = os.path.join(desktop, shortcut_name)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    shortcut.TargetPath = target_exe
    shortcut.WorkingDirectory = os.path.dirname(target_exe)
    shortcut.IconLocation = target_exe
    shortcut.save()

    print(f"✅ Shortcut created: {shortcut_path}")

def start_download(login, password, folder, callback=None, log_path="depot_log.txt",create_shortcut = False):
    base_dir = os.path.join(os.environ["LOCALAPPDATA"], "sque4")
    os.makedirs(base_dir, exist_ok=True)
    folder +="\SquadUe4"

    log_path = os.path.join(base_dir, "depot_log.txt")

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
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW

    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
        creationflags=creationflags
    )


    def emit(event, data=None):
        if callback:
            callback(event, data)

    def reader():
        try:
            with open(log_path, "r", encoding="cp1250", errors="replace") as f:
                f.seek(0, 2)

                last_line_time = time.time()
                start_download = False
                while True:
                    print("reading line.....")
                    line = f.readline()

                    if line:
                        last_line_time = time.time()  # reset timera

                        line = line.rstrip("\n")
                        lc = line.lower()

                        print("last line:", line)
                        emit("log", line)

                        # --- ERRORS DETECTION ---
                        if "steam guard" in lc or "auth code" in lc or "email" in lc:
                            emit("steam_guard", line)

                        if "invalidpassword" in lc:
                            emit("error", "invalid_password")
                            process.terminate()
                            break

                        if "ratelimit" in lc:
                            emit("error", "rate_limit")

                        if "initialize steam failed" in lc:
                            emit("error", "init_failed")

                        if "failed to allocate file" in lc:
                            print("error")
                            emit("error", "disk_full")
                            break
                        progress_match = re.search(r"(\d+(\.\d+)?)\s*%", line)
                        if progress_match:
                            percent = float(progress_match.group(1))
                            if percent >0 and start_download == False:
                                emit("page3")
                                start_download = True
                            if percent == 100:
                                if create_shortcut:
                                    create_shortcut_from_folder(folder)
                                emit("complete")
                                break
                            emit("progress", percent)
                    time.sleep(0.001)

        except Exception as e:
            print("error:", e)
            emit("error", str(e))



    t = threading.Thread(target=reader, daemon=True)
    t.start()

    return process, t

