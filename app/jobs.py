from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import uuid

from PIL import Image

from app.config import ENGINE_PATH, JOB_DIR, OUTPUT_DIR, UPLOAD_DIR
from app.print_math import PrintTarget, dpi_for_print, required_scale


@dataclass
class UpscaleJob:
    id: str
    status: str
    created_at: str
    input_name: str
    input_path: str
    output_path: str | None
    width_cm: float
    height_cm: float
    dpi: int
    model: str
    source_width: int | None = None
    source_height: int | None = None
    target_width: int | None = None
    target_height: int | None = None
    scale: int | None = None
    message: str | None = None


def ensure_dirs() -> None:
    for path in (UPLOAD_DIR, OUTPUT_DIR, JOB_DIR):
        path.mkdir(parents=True, exist_ok=True)


def job_path(job_id: str) -> Path:
    return JOB_DIR / f"{job_id}.json"


def save_job(job: UpscaleJob) -> None:
    ensure_dirs()
    job_path(job.id).write_text(json.dumps(asdict(job), indent=2), encoding="utf-8")


def load_job(job_id: str) -> UpscaleJob | None:
    path = job_path(job_id)
    if not path.exists():
        return None
    return UpscaleJob(**json.loads(path.read_text(encoding="utf-8")))


def create_job(input_name: str, upload_bytes: bytes, width_cm: float, height_cm: float, dpi: int, model: str) -> UpscaleJob:
    ensure_dirs()
    job_id = uuid.uuid4().hex
    suffix = Path(input_name).suffix.lower() or ".png"
    input_path = UPLOAD_DIR / f"{job_id}{suffix}"
    input_path.write_bytes(upload_bytes)

    job = UpscaleJob(
        id=job_id,
        status="queued",
        created_at=datetime.now(timezone.utc).isoformat(),
        input_name=input_name,
        input_path=str(input_path),
        output_path=None,
        width_cm=width_cm,
        height_cm=height_cm,
        dpi=dpi,
        model=model,
    )
    save_job(job)
    return job


def run_job(job_id: str) -> None:
    job = load_job(job_id)
    if job is None:
        return

    try:
        job.status = "running"
        job.message = "Preparing image."
        save_job(job)

        if not ENGINE_PATH.exists():
            job.status = "failed"
            job.message = (
                "Upscale engine is missing. Put realesrgan-ncnn-vulkan.exe in "
                "tools/realesrgan or set UPSCALE_ENGINE_PATH."
            )
            save_job(job)
            return

        input_path = Path(job.input_path)
        with Image.open(input_path) as image:
            source_width, source_height = image.size

        target = PrintTarget(job.width_cm, job.height_cm, job.dpi)
        scale = required_scale(source_width, source_height, target)
        output_path = OUTPUT_DIR / f"{job.id}.png"

        job.source_width = source_width
        job.source_height = source_height
        job.target_width = target.width_px
        job.target_height = target.height_px
        job.scale = scale
        job.output_path = str(output_path)
        job.message = f"Running Real-ESRGAN at {scale}x."
        save_job(job)

        if scale == 1:
            with Image.open(input_path) as image:
                image.save(output_path)
        else:
            command = [
                str(ENGINE_PATH),
                "-i",
                str(input_path),
                "-o",
                str(output_path),
                "-n",
                job.model,
                "-s",
                str(scale),
                "-f",
                "png",
            ]
            result = subprocess.run(command, cwd=str(ENGINE_PATH.parent), capture_output=True, text=True)
            if result.returncode != 0:
                job.status = "failed"
                job.message = result.stderr.strip() or result.stdout.strip() or "Upscale engine failed."
                save_job(job)
                return

        if not output_path.exists():
            job.status = "failed"
            job.message = "Engine finished but no output file was created."
            save_job(job)
            return

        with Image.open(output_path) as output:
            out_width, out_height = output.size

        dpi_info = dpi_for_print(out_width, out_height, job.width_cm, job.height_cm)
        job.status = "done"
        job.message = (
            f"Done. Output is {out_width}x{out_height}px, "
            f"effective print DPI: {dpi_info['effective_dpi']}."
        )
        save_job(job)
    except Exception as exc:
        job.status = "failed"
        job.message = str(exc)
        save_job(job)

