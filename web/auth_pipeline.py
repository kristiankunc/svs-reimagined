from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from .models import InvitedUser


def check_email_is_invited(backend, details, **kwargs):
    email = details.get("email")

    if get_user_model().objects.filter(email=email).exists():
        return

    if not InvitedUser.objects.filter(email=email).exists():
        messages.error(backend.strategy.request, "Email not invited, please contact the administrator.")
        return redirect("/")

    InvitedUser.objects.filter(email=email).delete()


def make_first_user_superuser(backend, user=None, **kwargs):
    User = get_user_model()
    if user and not User.objects.exclude(id=user.id).exists():
        user.is_superuser = True
        user.is_staff = True
        user.save()


def handle_social_auth_exception(request, exception):
    messages.error(request, str(exception))
    return redirect("/")
