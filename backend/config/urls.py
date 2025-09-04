from django.contrib import admin
from django.urls import include, path
from .api_docs import urlpatterns_docs

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("remover.urls")),
    # API docs (Swagger / ReDoc / OpenAPI JSON-YAML)
    *urlpatterns_docs,
]
