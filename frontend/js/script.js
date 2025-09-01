const imageInput = document.getElementById("imageInput");
const previewArea = document.getElementById("previewArea");
const removeBtn = document.getElementById("removeBtn");
const downloadBtn = document.getElementById("downloadBtn");
const dropArea = document.getElementById("dropArea");
const menuToggle = document.getElementById("menuToggle");
const nav = document.querySelector(".navbar nav");

const API_URL = "http://127.0.0.1:8000/api/remove-background/";

let uploadedFile = null;
let processedImageURL = null;

// Helpers
function setPreview(src, altText = "Preview") {
  if (!previewArea) return;
  const img = new Image();
  img.onload = () => {
    previewArea.classList.add("filled");
    previewArea.style.aspectRatio = `${img.naturalWidth} / ${img.naturalHeight}`;
    previewArea.innerHTML = "";
    img.alt = altText;
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "contain";
    previewArea.appendChild(img);
  };
  img.src = src;
}

function handleSelectedFile(file) {
  if (!file) return;
  uploadedFile = file;
  if (removeBtn) removeBtn.disabled = false;
  if (downloadBtn) downloadBtn.style.display = "none";

  const reader = new FileReader();
  reader.onload = (e) => setPreview(e.target.result, "Preview");
  reader.readAsDataURL(file);
}

function resetPreview(
  message = 'Drag & drop an image here or click "Upload Image"'
) {
  if (!previewArea) return;
  previewArea.classList.remove("filled");
  previewArea.style.aspectRatio = "";
  previewArea.innerHTML = `<p>${message}</p>`;
}

// Events
// File input → preview
if (imageInput && previewArea && removeBtn && downloadBtn) {
  imageInput.addEventListener("change", () => {
    const file = imageInput.files && imageInput.files[0];
    handleSelectedFile(file);
  });

  // Fetch API → process image
  removeBtn.addEventListener("click", async () => {
    if (!uploadedFile) return;

    removeBtn.disabled = true;
    const originalText = removeBtn.textContent;
    removeBtn.textContent = "Processing...";

    const formData = new FormData();
    formData.append("image", uploadedFile);

    try {
      const res = await fetch(API_URL, { method: "POST", body: formData });
      if (!res.ok) {
        let message = `Failed to process image (${res.status})`;
        try {
          const data = await res.json();
          if (data?.error) message = data.error;
        } catch (_) {}
        throw new Error(message);
      }

      const blob = await res.blob();
      processedImageURL = URL.createObjectURL(blob);

      setPreview(processedImageURL, "Processed");
      downloadBtn.href = processedImageURL;
      downloadBtn.style.display = "inline-block";
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      removeBtn.textContent = originalText;
      removeBtn.disabled = false;
    }
  });
}

// Drag and drop preview
if (dropArea && previewArea && removeBtn && downloadBtn) {
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, (e) => e.preventDefault());
    document.body.addEventListener(eventName, (e) => e.preventDefault());
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, () =>
      dropArea.classList.add("dragover")
    );
  });
  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, () =>
      dropArea.classList.remove("dragover")
    );
  });

  dropArea.addEventListener("drop", (e) => {
    const file =
      e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    handleSelectedFile(file);
  });
}

// Responsive navbar toggle
if (menuToggle && nav) {
  menuToggle.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}
