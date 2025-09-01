const imageInput = document.getElementById("imageInput");
const previewArea = document.getElementById("previewArea");
const removeBtn = document.getElementById("removeBtn");
const downloadBtn = document.getElementById("downloadBtn");

let uploadedFile = null;

// Events
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
