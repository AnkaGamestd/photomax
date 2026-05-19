$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv\Scripts\python.exe")) {
  throw "Virtual environment missing. Run .\scripts\setup.ps1 first."
}

Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000'"

& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
