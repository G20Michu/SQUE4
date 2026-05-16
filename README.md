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

### Warning

If the generated hash is different, the file has been modified or is not an official release.
### Project Python Version
Python 3.12.10
