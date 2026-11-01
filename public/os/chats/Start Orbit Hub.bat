@echo off
cd /d "%~dp0"
curl -sfL -m 8 -o "Your hub.new" "https://ashahmeetsworld.github.io/ashah-world/os/hub.html" 2>nul && move /y "Your hub.new" "Your hub.html" >nul
if exist "Your hub.new" del "Your hub.new"
if not exist "Your hub.html" if exist "..\04 Hub demo.html" copy /y "..\04 Hub demo.html" "Your hub.html" >nul
if not exist "Your hub.html" (
  echo Couldn't get your hub page. Check you're online and try again, or put this folder next to 04 Hub demo.html.
  pause
  exit /b
)
if not exist ".shortcut" (
  powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Orbit Hub.lnk');$s.TargetPath='%~f0';$s.WorkingDirectory='%~dp0';$s.WindowStyle=7;$s.Save()"
  echo made> ".shortcut"
)
if exist "%USERPROFILE%\.orbit\start.ps1" (
  powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%USERPROFILE%\.orbit\start.ps1" "%~dp0."
  exit /b
)
start "" "Your hub.html"
