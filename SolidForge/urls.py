"""
URL configuration for SolidForge project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings                # ✅ needed for MEDIA_URL and MEDIA_ROOT
from django.conf.urls.static import static       # ✅ needed for serving media files

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # 👈 link to your app's urls.py
]

# ✅ serve uploaded files (like profile pictures) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
