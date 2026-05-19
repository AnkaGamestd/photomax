$ErrorActionPreference = "Stop"

$EngineUrl = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip"
$ToolsDir = "tools\realesrgan"
$ZipPath = "tools\realesrgan-windows.zip"

New-Item -ItemType Directory -Force -Path "tools", $ToolsDir | Out-Null

$ExistingExe = "$ToolsDir\realesrgan-ncnn-vulkan.exe"
if (Test-Path $ExistingExe) {
  Write-Host "Engine already installed at $ExistingExe"
  exit 0
}

Write-Host "Downloading Real-ESRGAN ncnn Vulkan engine..."
Invoke-WebRequest -Uri $EngineUrl -OutFile $ZipPath

Write-Host "Extracting engine..."
if (Test-Path $ToolsDir) {
  Remove-Item -LiteralPath $ToolsDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $ToolsDir | Out-Null
Expand-Archive -LiteralPath $ZipPath -DestinationPath $ToolsDir -Force

$Exe = Get-ChildItem -Path $ToolsDir -Recurse -Filter "realesrgan-ncnn-vulkan.exe" | Select-Object -First 1
if ($null -eq $Exe) {
  throw "realesrgan-ncnn-vulkan.exe was not found after extraction."
}

if ($Exe.FullName -ne (Resolve-Path "$ToolsDir\realesrgan-ncnn-vulkan.exe" -ErrorAction SilentlyContinue)) {
  Copy-Item -LiteralPath $Exe.FullName -Destination "$ToolsDir\realesrgan-ncnn-vulkan.exe" -Force
}

Remove-Item -LiteralPath $ZipPath -Force

Write-Host "Engine installed at $ToolsDir\realesrgan-ncnn-vulkan.exe"
