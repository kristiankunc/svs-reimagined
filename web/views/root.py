from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def index(request):
    projects = []
    if request.user.is_authenticated:
        projects = request.user.projects.all()

    return render(request, "web/test.html", {"projects": projects})


def logout(request):
    auth_logout(request)
    return redirect("index")


urlpatterns = [
    path("", index, name="index"),
    path("logout/", logout, name="logout"),
]
