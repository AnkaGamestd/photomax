# Print Upscaler

Local web app for turning low-resolution images into print-sized outputs.

The app is intentionally local-first:

- Web UI runs on your PC.
- API can later be reused by a mobile app.
- Upscaling uses a real external engine, preferably `realesrgan-ncnn-vulkan`.
- If the engine is missing, the app reports that clearly instead of faking an AI result.

## Quick Start

```powershell
.\scripts\setup.ps1
.\scripts\run.ps1
```

Open:

```text
http://127.0.0.1:8000
```

## Real-ESRGAN Engine

Download the Windows release of `realesrgan-ncnn-vulkan` and place the executable at:

```text
tools\realesrgan\realesrgan-ncnn-vulkan.exe
```

Recommended first model:

```text
realesrgan-x4plus
```

You can also set a custom executable path:

```powershell
$env:UPSCALE_ENGINE_PATH="C:\path\to\realesrgan-ncnn-vulkan.exe"
```

## Print Targets

Approximate pixel targets:

| Size | 150 DPI | 200 DPI | 240 DPI | 300 DPI |
| --- | ---: | ---: | ---: | ---: |
| 50 x 70 cm | 2953 x 4134 | 3937 x 5512 | 4724 x 6614 | 5906 x 8268 |

For large wall prints, 200 DPI is often practical. Use 240-300 DPI when the print will be inspected closely.

