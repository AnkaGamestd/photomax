from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import ALLOWED_EXTENSIONS, ENGINE_PATH, MAX_UPLOAD_MB, STATIC_DIR
from app.jobs import create_job, ensure_dirs, load_job, run_job
from app.print_math import PrintTarget, dpi_for_print


app = FastAPI(title="Print Upscaler", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    ensure_dirs()


@app.get("/api/health")
def health() -> dict[str, object]:
    return {
        "ok": True,
        "engine_found": ENGINE_PATH.exists(),
        "engine_path": str(ENGINE_PATH),
    }


@app.get("/api/print-target")
def print_target(width_cm: float = 50, height_cm: float = 70, dpi: int = 200) -> dict[str, object]:
    target = PrintTarget(width_cm, height_cm, dpi)
    return {
        "width_cm": width_cm,
        "height_cm": height_cm,
        "dpi": dpi,
        "width_px": target.width_px,
        "height_px": target.height_px,
    }


@app.post("/api/jobs")
async def submit_job(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    width_cm: float = Form(50),
    height_cm: float = Form(70),
    dpi: int = Form(200),
    model: str = Form("realesrgan-x4plus"),
) -> dict[str, object]:
    suffix = Path(image.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and WEBP images are supported.")
    if width_cm <= 0 or height_cm <= 0:
        raise HTTPException(status_code=400, detail="Print dimensions must be positive.")
    if dpi not in {150, 200, 240, 300}:
        raise HTTPException(status_code=400, detail="DPI must be 150, 200, 240, or 300.")

    content = await image.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Image is larger than {MAX_UPLOAD_MB} MB.")

    job = create_job(image.filename or "upload.png", content, width_cm, height_cm, dpi, model)
    background_tasks.add_task(run_job, job.id)
    return {"job_id": job.id, "status": job.status}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, object]:
    job = load_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job.__dict__


@app.get("/api/jobs/{job_id}/download")
def download(job_id: str) -> FileResponse:
    job = load_job(job_id)
    if job is None or job.status != "done" or job.output_path is None:
        raise HTTPException(status_code=404, detail="Output not available.")
    return FileResponse(job.output_path, filename=f"print-upscaled-{job_id}.png", media_type="image/png")


@app.get("/api/dpi-check")
def dpi_check(width_px: int, height_px: int, width_cm: float = 50, height_cm: float = 70) -> dict[str, int]:
    return dpi_for_print(width_px, height_px, width_cm, height_cm)


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

