from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def index(request):
    return render(request, "web/test.html")


def logout(request):
    auth_logout(request)
    return redirect("index")


urlpatterns = [
    path("", index, name="index"),
    path("logout/", logout, name="logout"),
]
