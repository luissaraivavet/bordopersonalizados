@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 admin_server.py
) else (
  python admin_server.py
)
if errorlevel 1 pause
