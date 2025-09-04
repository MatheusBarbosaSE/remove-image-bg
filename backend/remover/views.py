from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from .serializers import ImageUploadSerializer
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io


class RemoveBackgroundView(GenericAPIView):
    """
    API endpoint to remove the background from an uploaded image.

    Features:
    - Accepts file uploads via multipart/form-data.
    - Validates input using ImageUploadSerializer.
    - Uses rembg to remove the background from the image.
    - Returns a PNG image with transparency preserved.
    - Provides clear error handling for invalid files or processing errors.

    This setup ensures the DRF Browsable API and Swagger/ReDoc
    can display a proper upload form.
    """

    # Tell DRF which serializer to use for validation
    serializer_class = ImageUploadSerializer

    # Ensure the endpoint accepts multipart form data for file uploads
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Validate incoming request using serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data["image"]

            try:
                # Open the uploaded image with Pillow
                input_image = Image.open(image_file)

                # Preserve the original format if possible, fallback to PNG
                image_format = input_image.format if input_image.format else "PNG"

                # Save input image to a buffer (as rembg expects bytes)
                buf_in = io.BytesIO()
                input_image.save(buf_in, format=image_format)

                # Run background removal with rembg
                output_bytes = remove(buf_in.getvalue())

                # Always return PNG with transparency preserved
                return HttpResponse(output_bytes, content_type="image/png")

            except UnidentifiedImageError:
                # The uploaded file is not a valid image
                return Response(
                    {"error": "The uploaded file is not a valid image."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except Exception as e:
                # Unexpected errors during processing
                return Response(
                    {"error": "Failed to process image.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # If serializer validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
