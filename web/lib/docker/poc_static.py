import tempfile
import threading
from git import Repo
from ...models import Project
from docker import errors as docker_errors
import docker
import time


def poc_create_static(project_id: int):
    project = Project.objects.get(id=project_id)

    thread = threading.Thread(target=run_static_project_creation, args=(project,))
    thread.start()


def run_static_project_creation(project):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(project.git_url, temp_dir, branch=project.git_branch)

        dockerfile_content = f"""
    FROM nginx:alpine
    COPY . /usr/share/nginx/html
    EXPOSE {project.port}
    CMD ["nginx", "-g", "daemon off;"]
    """
        with open(f"{temp_dir}/Dockerfile", "w") as dockerfile:
            dockerfile.write(dockerfile_content)

        dockerignore_content = """
    .git
    .gitignore
    Dockerfile
    .dockerignore
    """

        with open(f"{temp_dir}/.dockerignore", "w") as dockerignore:
            dockerignore.write(dockerignore_content)

        docker_client = docker.from_env()

        timestamp = int(time.time())
        unique_tag = f"{project.user.username}_{project.name}_{timestamp}"

        try:
            # Build the Docker image
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
                name=project.user.username + "_" + project.name,
            )
            print(f"Container {container.name} started successfully.")
        except docker_errors.APIError as e:
            print(f"Error starting container: {e}")
            return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary directory after all operations are complete
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"Temporary directory {temp_dir} cleaned up.")
