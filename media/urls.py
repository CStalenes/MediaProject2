"""
URLs pour l'app media.
"""
from django.urls import path
from media.views import UploadFileView

urlpatterns = [
    # Upload vers ImageKit - Juste file + fileName
    # Utilise l'API v2 ImageKit avec Basic Auth (base64)

    path('files/upload/', UploadFileView.as_view(), name='upload'),
]
