# SQUE4

SQUE4 is a Windows desktop application that automates downloading Squad game data using DepotDownloader and manages AppData switching between UE4 and UE5 environments. The application provides a simple graphical interface built with Tkinter.

---

## Features

- Steam login support  
- DepotDownloader integration (external compiled executable)  
- Steam Guard handling  
- Download progress tracking  
- Folder selection for installation  
- Optional desktop shortcut creation  
- AppData switcher (UE4 / UE5)  
- Real-time logs and status monitoring
- Logger in Appdata %localappdata% sque4/debug.log 
---

## EXE Integrity Check (SHA256)

To verify that the executable is original and has not been modified, follow the steps below.

### Open PowerShell in the folder containing `SQUE4.exe`:

```powershell
Get-FileHash "SQUE4.exe" -Algorithm SHA256
```

### Expected official hash:

```
4d8f790b3ef72cc266623163d508e63897f008b58f2c0090ab564d743d22f1d5
```

### ACE Approved release hash:

```
71AEAFAB6CA916FBB67446FDC24FE2FAF450C5D266D68DD698271E06585A1BE9
```

### Warning

If the generated hash is different, the file has been modified or is not an official release.
### Project Python Version
Python 3.12.10



## How to compile

1. Go to the Windows10-App directory.

2. Create a virtual environment:
```   
python -m venv .venv
```
3. Activate the virtual environment:
```   
.venv\Scripts\activate
```
4. Install required packages:
```   
pip install pyinstaller pywin32 psutil
```
5. Build the executable using PyInstaller:
```   
pyinstaller --onefile --noconsole --icon=icon.ico --add-data "Dependencies;Dependencies" --hidden-import=win32com --hidden-import=win32com.client --hidden-import=pythoncom --hidden-import=pywintypes --hidden-import=psutil SQUE4.py
```
After compilation, the executable will be in:
dist/SQUE4.exe

