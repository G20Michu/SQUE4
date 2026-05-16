import os
import re
import shutil
from .logger import Logger
logger = Logger()
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

