# SQUE4

SQUE4 is a Windows desktop application that automates downloading game data using DepotDownloader and manages AppData switching between UE4 and UE5 environments. The application provides a simple graphical interface built with Tkinter.

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

---

## EXE Integrity Check (SHA256)

To verify that the executable is original and has not been modified, follow the steps below.

### Open PowerShell in the folder containing `SQUE4.exe`:

```powershell
Get-FileHash "SQUE4.exe" -Algorithm SHA256
```

### Expected official hash:

```
823A11489568AF620A5068698FB9BE453B93FC33A8E4FDA8B495C2D0057BB4C0
```

### Warning

If the generated hash is different, the file has been modified or is not an official release.
