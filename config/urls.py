"""
URL configuration for Kigali Public Library (KPL) project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("", include("apps.core.urls")),
]

# Error Handlers
handler404 = "apps.core.views.custom_404"
handler403 = "apps.core.views.custom_403"
handler500 = "apps.core.views.custom_500"

# Gunicorn does not serve user uploads. This route covers membership
# documents, event images, and profile photos in production and development.
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG and settings.STATICFILES_DIRS:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )
