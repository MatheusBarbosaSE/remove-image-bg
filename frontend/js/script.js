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

// Events
// File input preview
if (imageInput && previewArea && removeBtn && downloadBtn) {
  imageInput.addEventListener("change", () => {
    const file = imageInput.files && imageInput.files[0];
    if (!file) return;

    uploadedFile = file;
    removeBtn.disabled = false;
    downloadBtn.style.display = "none";

    const reader = new FileReader();
    reader.onload = (e) => {
      previewArea.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
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

      previewArea.innerHTML = `<img src="${processedImageURL}" alt="Processed">`;
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
    if (!file) return;

    uploadedFile = file;
    removeBtn.disabled = false;
    downloadBtn.style.display = "none";

    const reader = new FileReader();
    reader.onload = (ev) => {
      previewArea.innerHTML = `<img src="${ev.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
  });
}

// Responsive navbar toggle
if (menuToggle && nav) {
  menuToggle.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
}
