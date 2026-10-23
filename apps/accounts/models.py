from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
    )
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    library_card_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="KPL Library Card ID if issued",
    )
    bio = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
