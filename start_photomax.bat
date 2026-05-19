@echo off
setlocal
cd /d "%~dp0"

echo.
echo PhotoMax local setup and launcher
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\setup.ps1"
if errorlevel 1 (
  echo.
  echo Setup failed.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\install_engine.ps1"
if errorlevel 1 (
  echo.
  echo Engine installation failed.
  pause
  exit /b 1
)

echo.
echo Starting PhotoMax at http://127.0.0.1:8000
echo Keep this window open while using the app.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\run.ps1"

echo.
echo PhotoMax stopped.
pause
