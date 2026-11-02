@echo off
cd /d "%~dp0"
set "ORBIT_HUB=%~dp0."
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://ashahmeetsworld.github.io/ashah-world/os/chats/turn-on.ps1 | iex"
pause
