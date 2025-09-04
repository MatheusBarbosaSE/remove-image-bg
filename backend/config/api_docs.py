from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Remove Image BG API",
        default_version="v1",
        description=(
            "OpenAPI schema for the background removal service. "
            "Upload an image and receive a transparent PNG with the background removed. "
            "Powered by rembg."
        ),
        contact=openapi.Contact(
            name="Matheus Barbosa", url="https://github.com/MatheusBarbosaSE"
        ),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns_docs = [
    # JSON/YAML raw schema
    re_path(
        r"^openapi(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # Swagger UI
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # ReDoc
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
