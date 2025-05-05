from django.db import models
from datetime import timedelta
from django.utils import timezone
import random


class InvitedUser(models.Model):
    def default_expires_at():
        return timezone.now() + timedelta(days=7)

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email", "created_at"]


class TemplateChoices(models.TextChoices):
    NONE = (
        "none",
        "None",
    )
    STATIC = (
        "static",
        "Static",
    )


class Project(models.Model):
    def generate_safe_port():
        used_ports = Project.objects.values_list("port", flat=True)
        available_ports = set(range(8000, 9000)) - set(used_ports)
        if available_ports:
            return random.choice(list(available_ports))
        raise ValueError("No available ports in the safe range.")

    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    git_url = models.URLField()
    git_branch = models.CharField(max_length=255, default="main")
    template = models.CharField(
        max_length=50,
        choices=TemplateChoices.choices,
        default=TemplateChoices.NONE,
    )

    port = models.IntegerField(default=generate_safe_port)
