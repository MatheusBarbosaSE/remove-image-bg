from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RemoveBackgroundView(APIView):
    def post(self, request, format=None):
        return Response({"message": "Endpoint is alive"}, status=status.HTTP_200_OK)
