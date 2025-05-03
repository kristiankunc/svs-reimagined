from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import InvitedUser
from ...auth_pipeline import is_user_registered, is_user_invited, is_first_user


class AuthPipelineTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_model.objects.create_user(
            username="registered", email="registered@example.com", password="password123"
        )
        InvitedUser.objects.create(email="invited@example.com")

    def test_is_user_registered(self):
        self.assertTrue(is_user_registered("registered@example.com"))
        self.assertFalse(is_user_registered("nonexistent@example.com"))

    def test_is_user_invited(self):
        self.assertTrue(is_user_invited("invited@example.com"))
        self.assertFalse(is_user_invited("nonexistent@example.com"))

    def test_is_first_user(self):
        self.user_model.objects.all().delete()

        first_user = self.user_model.objects.create_user(
            username="firstuser", email="firstuser@example.com", password="password123"
        )
        self.assertTrue(is_first_user(first_user))

        second_user = self.user_model.objects.create_user(
            username="seconduser", email="seconduser@example.com", password="password123"
        )
        self.assertFalse(is_first_user(second_user))
