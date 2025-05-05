from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .forms import ProjectForm
from .models import Project
from .lib.docker.poc_static import poc_create_static


def index(request):
    return render(request, "web/test.html")


def logout(request):
    auth_logout(request)
    return redirect("index")


def create(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            print(form.cleaned_data)

            project = Project(
                name=form.cleaned_data["name"],
                git_url=form.cleaned_data["git_url"],
                git_branch=form.cleaned_data["git_branch"],
                template=form.cleaned_data["template"],
                user=request.user,
            )
            project.save()

            poc_create_static(project.id)
            return redirect("index")

    return render(request, "web/create.html", {"form": form})


def project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, "web/project.html", {"project": project})
