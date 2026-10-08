"""
Root URL configuration for Glow & Grace.

The admin is mounted at /admin/.
Everything else falls through to the 'products' app's URLconf.
In DEBUG, media files (uploaded product images) are served by Django
straight from MEDIA_ROOT so you can see uploads without extra config.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
]


# Serve uploaded media during development only.
# On Render, media is served from Cloudinary (or Render Disk) — not from here.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ---------------------------------------------------------------------------
# Admin branding — what you and your staff see at /admin/
# ---------------------------------------------------------------------------
admin.site.site_header = "Glow & Grace Administration"
admin.site.site_title = "Glow & Grace Admin"
admin.site.index_title = "Manage your store"