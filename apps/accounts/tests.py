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
