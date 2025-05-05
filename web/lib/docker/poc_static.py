import tempfile
import threading
from git import Repo
from docker import errors as docker_errors
import docker
import shutil
import time

from ...models import Project
from .dockerfile_templates.template_manager import Template


def poc_create_static(project_id: int):
    project = Project.objects.get(id=project_id)

    thread = threading.Thread(target=run_static_project_creation, args=(project,))
    thread.start()


def run_static_project_creation(project):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(project.git_url, temp_dir, branch=project.git_branch)

        template = Template.get(Template.TemplateType.STATIC)
        template.apply_variables({"port": project.port})
        with open(f"{temp_dir}/Dockerfile", "w") as dockerfile:
            dockerfile.write(template.dockerfile_content)

        with open(f"{temp_dir}/.dockerignore", "w") as dockerignore:
            dockerignore.write(template.dockerignore_content)

        docker_client = docker.from_env()

        timestamp = int(time.time())
        unique_tag = f"{project.id}_{timestamp}"

        try:
            image = docker_client.images.build(
                path=temp_dir, tag=unique_tag, rm=True, container_limits={"memory": 256 * 1024 * 1024}
            )[0]
            print(f"Image {image.tags[0]} built successfully.")
        except Exception as e:
            print(f"Error building image: {e}")
            return

        try:
            # Run the Docker container
            container = docker_client.containers.run(
                image=image,
                ports={"80/tcp": ("127.0.0.1", project.port)},
                detach=True,
                labels={"caddy": f"{project.name}.svs.gyarab.cz", "caddy.reverse_proxy": "{{upstreams 80}}"},
                name=project.id,
            )
            print(f"Container {container.name} started successfully.")
        except docker_errors.APIError as e:
            print(f"Error starting container: {e}")
            return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"Temporary directory {temp_dir} cleaned up.")


def poc_delete_static(project_id: int):
    project = Project.objects.get(id=project_id)

    try:
        docker_client = docker.from_env()
        container = docker_client.containers.get(str(project.id))
        container.stop()
        container.remove(force=True)
        print(f"Container {container.name} stopped and removed successfully.")
    except docker_errors.NotFound:
        print(f"Container {project.id} not found.")
    except Exception as e:
        print(f"An error occurred while stopping/removing the container: {e}")
