import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a default superuser from environment variables if one doesn't already exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
        email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@kplonline.org")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD")

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser '{username}' already exists. Skipping.")
            )
            return

        if not password:
            if settings.DEBUG:
                password = "KPLAdmin@2026#Secure!"
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "DEFAULT_ADMIN_PASSWORD is not set, so no superuser was created. "
                        "Set it and redeploy, or run: python manage.py createsuperuser"
                    )
                )
                return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created superuser '{username}' ({email})")
        )
