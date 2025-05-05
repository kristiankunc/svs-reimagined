import os


class Template:
    class TemplateType:
        STATIC = "static"

        @classmethod
        def exists(cls, value: str) -> bool:
            return value in cls.__dict__.values()

    def __init__(self, template_type: TemplateType, dockerfile_content: str, dockerignore_content: str):
        self.template_type = template_type
        self.dockerfile_content = dockerfile_content
        self.dockerignore_content = dockerignore_content

    # TODO: maybe use something better than {{key}}
    def apply_variables(self, variables: dict) -> bool:
        for key, value in variables.items():
            self.dockerfile_content = self.dockerfile_content.replace(f"{{{key}}}", str(value))
            self.dockerignore_content = self.dockerignore_content.replace(f"{{{key}}}", str(value))

        if "{{" in self.dockerfile_content or "{{" in self.dockerignore_content:
            raise ValueError("Not all variables were replaced in the template.")

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
