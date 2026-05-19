$ErrorActionPreference = "Stop"

$Python = "C:\Users\desig\AppData\Local\Programs\Python\Python314\python.exe"

if (!(Test-Path $Python)) {
  throw "Python not found at $Python"
}

if (!(Test-Path ".venv")) {
  & $Python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

New-Item -ItemType Directory -Force -Path "data\uploads", "data\outputs", "data\jobs", "tools\realesrgan" | Out-Null

Write-Host "Setup complete."

