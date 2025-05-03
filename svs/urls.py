from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("social_django.urls", namespace="social")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("web.urls")),
]
