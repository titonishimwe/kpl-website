import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Runs on every Render deploy (build.sh).

    - If the admin account does not exist yet, it is created from the environment.
    - If it exists, its username, email and password are left exactly as they are,
      so redeploying never changes how the admin signs in. Only the access flags
      (active / staff / superuser) are restored in case they were switched off.
    - The password is overwritten only when DEFAULT_ADMIN_RESET_PASSWORD=true is set
      on purpose, and only if it differs from DEFAULT_ADMIN_PASSWORD.
    """

    help = "Create the default superuser if missing; never change an existing admin's credentials"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
        email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@kplonline.org")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        reset_password = os.getenv("DEFAULT_ADMIN_RESET_PASSWORD", "False").strip().lower() == "true"

        user = User.objects.filter(username=username).first()
        if user:
            changed = [
                flag for flag in ("is_active", "is_staff", "is_superuser") if not getattr(user, flag)
            ]
            for flag in changed:
                setattr(user, flag, True)
            if not user.email:
                user.email = email  # fill a missing email; never replace an existing one
                changed.append("email")

            message = f"Superuser '{username}' already exists. Username, email and password kept."
            if reset_password:
                if not password:
                    self.stdout.write(self.style.WARNING(
                        "DEFAULT_ADMIN_RESET_PASSWORD is true but DEFAULT_ADMIN_PASSWORD is not set; password not changed."
                    ))
                elif user.check_password(password):
                    self.stdout.write(self.style.WARNING(
                        "DEFAULT_ADMIN_RESET_PASSWORD is true but the password already matches; nothing to reset. "
                        "Set DEFAULT_ADMIN_RESET_PASSWORD back to false in Render."
                    ))
                else:
                    user.set_password(password)
                    changed.append("password")
                    message = f"Password for superuser '{username}' was RESET from DEFAULT_ADMIN_PASSWORD."
                    self.stdout.write(self.style.WARNING(
                        "DEFAULT_ADMIN_RESET_PASSWORD is true. Set it back to false in Render now, "
                        "or the next deploy will undo any password change made in the meantime."
                    ))

            if changed:
                user.save(update_fields=changed)
            self.stdout.write(self.style.SUCCESS(message))
            return

        if not password:
            if settings.DEBUG:
                password = "KPLAdmin@2026#Secure!"
            else:
                self.stdout.write(self.style.WARNING(
                    "DEFAULT_ADMIN_PASSWORD is not set, so no superuser was created. "
                    "Set it and redeploy, or run: python manage.py createsuperuser"
                ))
                return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Successfully created superuser '{username}' ({email})"))
