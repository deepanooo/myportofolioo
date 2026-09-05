from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import landing_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page, name="landing_page"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )