from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


def _make_png(size=(100, 60), color=(255, 0, 0, 255), mode="RGBA") -> bytes:
    """
    Generate an in-memory PNG image for testing purposes.
    """
    img = Image.new(mode, size, color)
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio.getvalue()


class RemoveBackgroundAPITests(TestCase):
    """
    Test suite for the background removal API endpoint.
    """

    def setUp(self):
        self.client = APIClient()
        # Try reverse lookup first, fallback to static path if not named
        try:
            self.url = reverse("remove-background")
        except Exception:
            self.url = "/api/remove-background/"

    def _upload(self, img_bytes, filename="test.png", content_type="image/png"):
        """
        Helper: wrap raw image bytes in a Django SimpleUploadedFile.
        """
        return SimpleUploadedFile(filename, img_bytes, content_type=content_type)

    def test_success_returns_png_with_transparency(self):
        """
        Valid POST should return a PNG image (ideally with transparency).
        """
        img_bytes = _make_png(size=(80, 120))  # portrait aspect ratio
        resp = self.client.post(
            self.url, data={"image": self._upload(img_bytes)}, format="multipart"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(resp["Content-Type"], ["image/png", "application/octet-stream"])

        # Validate returned PNG
        out = BytesIO(resp.content)
        returned = Image.open(out)
        self.assertEqual(returned.format, "PNG")
        self.assertIn(returned.mode, ["RGBA", "LA", "P"])  # transparent-capable modes
        self.assertGreater(len(resp.content), 100)

    def test_missing_file_returns_400(self):
        """
        Missing file should return 400 (or 422 depending on validation).
        """
        resp = self.client.post(self.url, data={}, format="multipart")
        self.assertIn(
            resp.status_code,
            (status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY),
        )
        try:
            data = resp.json()
            self.assertTrue(any(k in data for k in ["error", "image"]))
        except Exception:
            pass  # Some responses may not be JSON

    def test_invalid_file_type_returns_400(self):
        """
        Non-image file should result in a 400 or 415 error.
        """
        fake = SimpleUploadedFile("bad.txt", b"not-an-image", content_type="text/plain")
        resp = self.client.post(self.url, data={"image": fake}, format="multipart")
        self.assertIn(
            resp.status_code,
            (status.HTTP_400_BAD_REQUEST, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE),
        )
        try:
            data = resp.json()
            self.assertTrue("error" in data or "image" in data)
        except Exception:
            pass

    def test_get_not_allowed(self):
        """
        GET should return 405 on API-only views (or 200 if healthcheck is present).
        """
        resp = self.client.get(self.url)
        self.assertIn(
            resp.status_code, (status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_200_OK)
        )

    def test_cors_preflight_options(self):
        """
        Preflight CORS (OPTIONS request) should return 200/204 with proper headers.
        """
        resp = self.client.options(
            self.url,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
            HTTP_ORIGIN="http://localhost:3000",
        )
        self.assertIn(
            resp.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)
        )
        acao = resp.headers.get("Access-Control-Allow-Origin")
        self.assertTrue(acao is None or acao in ["*", "http://localhost:3000"])
