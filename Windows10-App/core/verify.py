import os
import re
import shutil

def base_dir():
    base = os.path.join(os.environ["LOCALAPPDATA"], "SquadGame")
    return base

def CreateAppData():
    base_dir = os.path.join(os.environ["LOCALAPPDATA"])


    print("BASE:", base_dir)

    path1 = os.path.join(base_dir, "sque4", "UE4_BACKUP")
    path2 = os.path.join(base_dir, "sque4", "UE5_BACKUP")

    print("CREATING:", path1)
    print("CREATING:", path2)

    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)


def VerifySquadAppdata():
    file_path = os.path.join(
        base_dir(),
        "Saved",
        "SaveGames",
        "SquadUI.sav"
    )

    print(file_path)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        if re.search(r"UE4", content):
            print("FOUND UE4 4.27")
            return "UE4"

        elif re.search(r"Squad/v10", content):
            print("FOUND UE5")
            return "UE5"

        else:
            print("NO UE VERSION FOUND")
            return None

    except FileNotFoundError:
        print("No Appdata file found")
        return None

def create_backup_appdata():

    base_dir = os.path.join(os.environ["LOCALAPPDATA"], "sque4")
    ue5_backup_path = os.path.join(
        base_dir,
        "UE5_APPDATA"
    )
    eu4_backup_path = os.path.join(
        base_dir,
        "EU4_APPDATA"
    )
def is_folder_locked(path):
    try:
        if os.path.exists:
            return False
        test_path = path + "_test"
        os.rename(path, test_path)
        os.rename(test_path, path)
        return False
    except OSError:
        return True

def switch_appdata():
    backup_root = os.path.join(os.environ["LOCALAPPDATA"], "sque4")
    squad_root = os.path.join(os.environ["LOCALAPPDATA"], "SquadGame")
    appdata_root = os.path.join(os.environ["LOCALAPPDATA"])
    ue5_backup = os.path.join(backup_root, "UE5_APPDATA")
    ue4_backup = os.path.join(backup_root, "UE4_APPDATA")

    os.makedirs(ue5_backup, exist_ok=True)
    os.makedirs(ue4_backup, exist_ok=True)

    if is_folder_locked(squad_root):
        print(" Folder jest używany przez grę! Zamknij Squad.")
        return

    engine = VerifySquadAppdata()

    if os.path.exists(squad_root):
        if engine == "UE5":
            shutil.rmtree(ue5_backup)
            shutil.move(squad_root, ue5_backup,)
            if os.path.exists(ue4_backup):
                shutil.copytree(ue4_backup, squad_root,dirs_exist_ok=True)
        elif engine == "UE4":
            shutil.rmtree(ue4_backup)
            shutil.move(squad_root, ue4_backup)
            if os.path.exists(ue5_backup):
                shutil.copytree(ue5_backup, squad_root,dirs_exist_ok=True)


def verify():
    VerifySquadAppdata()

#switch_appdata()
#verify()
#CreateAppData()