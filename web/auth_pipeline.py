from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from web.models import InvitedUser


def is_user_registered(email: str) -> bool:
    return get_user_model().objects.filter(email=email).exists()


def is_user_invited(email: str) -> bool:
    return InvitedUser.objects.filter(email=email).exists()


def is_first_user(user) -> bool:
    User = get_user_model()
    return not User.objects.exclude(id=user.id).exists()


def check_email_is_invited(backend, details, **kwargs):
    email = details.get("email")

    if is_user_registered(email):
        return

    if not is_user_invited(email):
        messages.error(backend.strategy.request, "Email not invited, please contact the administrator.")
        return redirect("/")

    InvitedUser.objects.filter(email=email).delete()


def make_first_user_superuser(backend, user=None, **kwargs):
    if user and is_first_user(user):
        user.is_superuser = True
        user.is_staff = True
        user.save()
