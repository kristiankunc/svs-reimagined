import os


class Template:
    class TemplateType:
        STATIC = "static"

        @classmethod
        def exists(cls, value: str) -> bool:
            return value in cls.__dict__.values()

    template_type: TemplateType
    dockerfile_content: str
    dockerignore_content: str

    @staticmethod
    def get(type: TemplateType) -> "Template":
        if not Template.TemplateType.exists(type):
            raise ValueError(f"Invalid template type: {type}")

        template_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), type)

        if not os.path.exists(template_directory):
            raise FileNotFoundError(f"Template directory does not exist: {template_directory}")

        with open(os.path.join(template_directory, "Dockerfile"), "r") as dockerfile:
            dockerfile_content = dockerfile.read()

        with open(os.path.join(template_directory, ".dockerignore"), "r") as dockerignore:
            dockerignore_content = dockerignore.read()

        return Template(
            template_type=type,
            dockerfile_content=dockerfile_content,
            dockerignore_content=dockerignore_content,
        )
