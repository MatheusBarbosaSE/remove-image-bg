from django.conf import settings
from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    # Limits
    MAX_UPLOAD_SIZE = getattr(settings, "MAX_UPLOAD_SIZE", 5 * 1024 * 1024)
    ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

    def validate_image(self, file):
        # Size check
        size = getattr(file, "size", None)
        if size is not None and size > self.MAX_UPLOAD_SIZE:
            mb = self.MAX_UPLOAD_SIZE // (1024 * 1024)
            raise serializers.ValidationError(
                f"Image too large. Maximum allowed size is {mb} MB."
            )

        # Content-type check (when available)
        ctype = getattr(file, "content_type", None)
        if ctype and ctype not in self.ALLOWED_CONTENT_TYPES:
            allowed = ", ".join(sorted(self.ALLOWED_CONTENT_TYPES))
            raise serializers.ValidationError(
                f"Unsupported file type. Allowed: {allowed}"
            )

        return file
