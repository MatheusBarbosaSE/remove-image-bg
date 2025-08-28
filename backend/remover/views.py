from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io
from django.http import HttpResponse

class RemoveBackgroundView(APIView):
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            try:
                # Open the uploaded image
                input_image = Image.open(image_file)

                # Preserve original format if possible; fall back to PNG
                image_format = input_image.format if input_image.format else 'PNG'

                # Convert image to bytes (as rembg expects bytes)
                image_bytes = io.BytesIO()
                input_image.save(image_bytes, format=image_format)

                # Process with rembg
                output_bytes = remove(image_bytes.getvalue())

                # Always return PNG to guarantee transparency
                return HttpResponse(output_bytes, content_type='image/png')

            except UnidentifiedImageError:
                return Response(
                    {"error": "The uploaded file is not a valid image."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                # Avoid leaking internals; keep a short detail for debugging
                return Response(
                    {"error": "Failed to process image.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
