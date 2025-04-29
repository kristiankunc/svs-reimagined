from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("oauth/", include("social_django.urls", namespace="social")),
    path("", views.index, name="index"),
]
