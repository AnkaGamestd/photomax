from pathlib import Path
import os


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
OUTPUT_DIR = DATA_DIR / "outputs"
JOB_DIR = DATA_DIR / "jobs"
STATIC_DIR = ROOT_DIR / "static"

DEFAULT_ENGINE_PATH = ROOT_DIR / "tools" / "realesrgan" / "realesrgan-ncnn-vulkan.exe"
ENGINE_PATH = Path(os.getenv("UPSCALE_ENGINE_PATH", str(DEFAULT_ENGINE_PATH)))

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "80"))

