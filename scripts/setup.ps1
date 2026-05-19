$ErrorActionPreference = "Stop"

function Test-Python {
  param(
    [string]$Command,
    [string[]]$Arguments = @()
  )

  try {
    & $Command @Arguments --version | Out-Null
    return $LASTEXITCODE -eq 0
  } catch {
    return $false
  }
}

function Set-PythonCommand {
  if ($env:PHOTOMAX_PYTHON -and (Test-Path $env:PHOTOMAX_PYTHON)) {
    $script:PythonCommand = $env:PHOTOMAX_PYTHON
    $script:PythonArguments = @()
    return
  }

  if (Test-Python "py" @("-3")) {
    $script:PythonCommand = "py"
    $script:PythonArguments = @("-3")
    return
  }

  if (Test-Python "python") {
    $script:PythonCommand = "python"
    $script:PythonArguments = @()
    return
  }

  throw "Python was not found. Install Python 3.12+ and make sure 'Add python.exe to PATH' is enabled, or set PHOTOMAX_PYTHON to python.exe."
}

function Invoke-BasePython {
  & $script:PythonCommand @script:PythonArguments @args
}

Set-PythonCommand
Write-Host "Using Python:"
Invoke-BasePython --version

if (!(Test-Path ".venv")) {
  Invoke-BasePython -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

New-Item -ItemType Directory -Force -Path "data\uploads", "data\outputs", "data\jobs", "tools\realesrgan" | Out-Null

Write-Host "Setup complete."
