const imageInput = document.getElementById("imageInput");
const previewArea = document.getElementById("previewArea");
const removeBtn = document.getElementById("removeBtn");
const downloadBtn = document.getElementById("downloadBtn");
const dropArea = document.getElementById("dropArea");

let uploadedFile = null;

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
