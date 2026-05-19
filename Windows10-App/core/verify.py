import os
import re
import shutil
from .logger import Logger
import winreg

logger = Logger()

#------------ steam ----------------
def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        value, _ = winreg.QueryValueEx(key, "InstallPath")
        return value
    except:
        # fallback
        logger.warning("steam path not found in winreg")
        default = r"C:\Program Files (x86)\Steam"
        if os.path.exists(default):
            return default
    logger.warning("no steam path found")
    return None


def get_libraries(steam_path):
    libraries = [steam_path]

    vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

    if not os.path.exists(vdf_path):
        return libraries

    with open(vdf_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":\\" in line:
                path = line.split('"')[3]
                path = path.replace("\\\\", "\\")
                libraries.append(path)

    return libraries


def VerifySquadMod(squad_mod_id: int):
    steam_path = get_steam_path()

    if not steam_path:
        logger.warning("Steam not found")
        return False

    libraries = get_libraries(steam_path)

    for lib in libraries:
        workshop_path = os.path.join(lib, "steamapps", "workshop", "content", "393380")

        if os.path.exists(workshop_path):
            logger.info(f"Found path: {workshop_path}")

            for mod in os.listdir(workshop_path):
                full_path = os.path.join(workshop_path, mod)
                if os.path.isdir(full_path):
                    logger.info(f"  Mod: {full_path}")
                    if str(squad_mod_id) in full_path:
                        return True

    return False

#------------- appdata ----------------
def base_dir():
    base = os.path.join(os.environ["LOCALAPPDATA"], "SquadGame")
    return base

def CreateAppData():
    base_dir = os.path.join(os.environ["LOCALAPPDATA"])

    logger.info("Base dir",base_dir)

    path1 = os.path.join(base_dir, "sque4", "UE4_BACKUP")
    path2 = os.path.join(base_dir, "sque4", "UE5_BACKUP")
    logger.info("EU4_BACKUP path",path1)
    logger.info("EU5_BACKUP path",path2)

    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)


def VerifySquadAppdata():
    file_path = os.path.join(
        base_dir(),
        "Saved",
        "SaveGames",
        "SquadUI.sav"
    )

    logger.info("Squad appdata file path" + file_path)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        if re.search(r"UE4", content):
            logger.info("FOUND UE4 appdata")
            return "UE4"

        elif re.search(r"Squad/v10", content):
            logger.info("FOUND UE5 appdata")
            return "UE5"

        else:
            logger.warning("NO UE VERSION FOUND")
            return None

    except FileNotFoundError:
        logger.warning("No Appdata file found")
        return None


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
        logger.error("file locked by other exe " , path )
        return

    engine = VerifySquadAppdata()

    if os.path.exists(squad_root):
        if engine == "UE5":
            shutil.rmtree(ue5_backup)
            shutil.move(squad_root, ue5_backup,)
            if os.path.exists(ue4_backup):
                shutil.copytree(ue4_backup, squad_root,dirs_exist_ok=True)
            logger.info("appdata changed from UE5 to UE4")
        elif engine == "UE4":
            shutil.rmtree(ue4_backup)
            shutil.move(squad_root, ue4_backup)
            if os.path.exists(ue5_backup):
                shutil.copytree(ue5_backup, squad_root,dirs_exist_ok=True)
            logger.info("appdata changed from UE4 to UE5")

