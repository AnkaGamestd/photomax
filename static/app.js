const engineStatus = document.querySelector("#engineStatus");
const uploadForm = document.querySelector("#uploadForm");
const imageInput = document.querySelector("#imageInput");
const preview = document.querySelector("#preview");
const dropzone = document.querySelector(".dropzone");
const sizePreset = document.querySelector("#sizePreset");
const widthCm = document.querySelector("#widthCm");
const heightCm = document.querySelector("#heightCm");
const dpi = document.querySelector("#dpi");
const model = document.querySelector("#model");
const targetInfo = document.querySelector("#targetInfo");
const jobStatus = document.querySelector("#jobStatus");
const downloadLink = document.querySelector("#downloadLink");

const presets = {
  "50x70": [50, 70],
  "40x60": [40, 60],
  "30x40": [30, 40],
};

async function refreshHealth() {
  const response = await fetch("/api/health");
  const health = await response.json();
  engineStatus.classList.toggle("ok", health.engine_found);
  engineStatus.classList.toggle("fail", !health.engine_found);
  engineStatus.textContent = health.engine_found ? "Engine ready" : "Engine missing";
}

async function refreshTarget() {
  const params = new URLSearchParams({
    width_cm: widthCm.value,
    height_cm: heightCm.value,
    dpi: dpi.value,
  });
  const response = await fetch(`/api/print-target?${params}`);
  const target = await response.json();
  targetInfo.textContent = `${target.width_cm} x ${target.height_cm} cm / ${target.dpi} DPI hedefi: ${target.width_px} x ${target.height_px} px`;
}

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;

  preview.src = URL.createObjectURL(file);
  dropzone.classList.add("has-image");
});

sizePreset.addEventListener("change", () => {
  if (sizePreset.value !== "custom") {
    const [w, h] = presets[sizePreset.value];
    widthCm.value = w;
    heightCm.value = h;
  }
  refreshTarget();
});

[widthCm, heightCm].forEach((input) => {
  input.addEventListener("input", () => {
    sizePreset.value = "custom";
    refreshTarget();
  });
});

dpi.addEventListener("change", refreshTarget);

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  downloadLink.classList.add("hidden");

  const file = imageInput.files[0];
  if (!file) {
    jobStatus.textContent = "Önce bir görsel seç.";
    return;
  }

  const submitButton = uploadForm.querySelector("button");
  submitButton.disabled = true;
  jobStatus.textContent = "İş kuyruğa alınıyor.";

  const formData = new FormData();
  formData.append("image", file);
  formData.append("width_cm", widthCm.value);
  formData.append("height_cm", heightCm.value);
  formData.append("dpi", dpi.value);
  formData.append("model", model.value);

  try {
    const response = await fetch("/api/jobs", { method: "POST", body: formData });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed.");
    }
    const job = await response.json();
    await pollJob(job.job_id);
  } catch (error) {
    jobStatus.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});

async function pollJob(jobId) {
  while (true) {
    const response = await fetch(`/api/jobs/${jobId}`);
    const job = await response.json();
    jobStatus.textContent = job.message || `Durum: ${job.status}`;

    if (job.status === "done") {
      downloadLink.href = `/api/jobs/${jobId}/download`;
      downloadLink.classList.remove("hidden");
      return;
    }

    if (job.status === "failed") {
      return;
    }

    await new Promise((resolve) => setTimeout(resolve, 1200));
  }
}

refreshHealth();
refreshTarget();
