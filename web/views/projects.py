from django.urls import path

from django.shortcuts import render, redirect
from web.forms import ProjectForm
from web.models import Project
from web.lib.docker.poc_static import poc_create_static, poc_delete_static
from web.lib.docker.container_info import ContainerInfo


def create_project(request):
    if not request.user.is_authenticated:
        return redirect("index")

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
    if not request.user.is_authenticated or not Project.objects.filter(id=project_id, user=request.user).exists():
        return redirect("index")

    project = Project.objects.get(id=project_id, user=request.user)
    logs = None
    if ContainerInfo.exists(project.id):
        logs = ContainerInfo.get_logs(project.id) if project else None

    return render(request, "web/project.html", {"project": project, "logs": logs})


def delete_project(request, project_id):
    if request.method == "POST" and request.user.is_authenticated:
        project = Project.objects.get(id=project_id, user=request.user)
        if project:
            poc_delete_static(project.id)
            project.delete()
            return redirect("index")


urlpatterns = [
    path("create_project/", create_project, name="create_project"),
    path("project/<int:project_id>/", project, name="project"),
    path("project/<int:project_id>/delete/", delete_project, name="delete_project"),
]
