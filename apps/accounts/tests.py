import os
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTest(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Member Sign In")

    def test_register_page_loads(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")

    def test_user_registration(self):
        data = {
            "first_name": "Aline",
            "last_name": "Uwase",
            "username": "aline",
            "email": "aline@example.com",
            "password1": "SecurePass@2026#",
            "password2": "SecurePass@2026#",
        }
        response = self.client.post(reverse("accounts:register"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="aline").exists())
        user = User.objects.get(username="aline")
        self.assertTrue(hasattr(user, "profile"))


class CreateDefaultAdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "OldPass@2026#")

    def run_command(self, **env):
        env = {
            "DEFAULT_ADMIN_USERNAME": "admin",
            "DEFAULT_ADMIN_PASSWORD": "NewPass@2026#",
            "DEFAULT_ADMIN_RESET_PASSWORD": "false",
            **env,
        }
        with mock.patch.dict(os.environ, env):
            call_command("create_default_admin")
        self.admin.refresh_from_db()

    def test_existing_admin_password_is_kept_by_default(self):
        self.run_command()
        self.assertTrue(self.admin.check_password("OldPass@2026#"))

    def test_existing_admin_password_is_reset_when_requested(self):
        self.run_command(DEFAULT_ADMIN_RESET_PASSWORD="true")
        self.assertTrue(self.admin.check_password("NewPass@2026#"))

    def test_reset_makes_a_disabled_account_usable(self):
        User.objects.filter(pk=self.admin.pk).update(is_active=False, is_staff=False)
        self.run_command(DEFAULT_ADMIN_RESET_PASSWORD="true")
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_staff)
