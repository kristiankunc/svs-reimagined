from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout, name="logout"),
    path("create/", views.create, name="create"),
]
