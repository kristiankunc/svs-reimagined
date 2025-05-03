from django.db import models
from django.contrib import admin
from datetime import timedelta
from django.utils import timezone


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


@admin.register(InvitedUser)
class InvitedUserAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "expires_at")
    ordering = ("email", "created_at")
