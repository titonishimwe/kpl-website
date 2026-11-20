import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    """Turn "New Arrivals" into "Staff Picks" (keeping existing rows) and add impact stats."""

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel("BookArrival", "StaffPick"),
        migrations.AlterModelOptions(
            name="staffpick",
            options={
                "ordering": ["category", "order", "title"],
                "verbose_name": "staff pick",
                "verbose_name_plural": "staff picks",
            },
        ),
        migrations.AddField(
            model_name="staffpick",
            name="author",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="staffpick",
            name="recommended_by",
            field=models.CharField(
                blank=True,
                help_text="Staff member's first name, e.g. 'Aline, Children's Librarian'",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="staffpick",
            name="note",
            field=models.CharField(
                blank=True,
                help_text="One or two sentences on why the team recommends this book.",
                max_length=240,
            ),
        ),
        migrations.AddField(
            model_name="staffpick",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Show on homepage"),
        ),
        migrations.AddField(
            model_name="staffpick",
            name="added_on",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name="ImpactStat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(help_text="As it should appear, e.g. '120,000+' or '3.5K'", max_length=30)),
                ("label", models.CharField(help_text="e.g. 'Library visitors in 2025'", max_length=80)),
                (
                    "icon",
                    models.CharField(
                        choices=[
                            ("people", "Visitors"),
                            ("person-vcard", "Members"),
                            ("book", "Books"),
                            ("laptop", "Digital resources"),
                            ("emoji-smile", "Children & youth"),
                            ("calendar-event", "Events"),
                            ("building", "Libraries"),
                            ("award", "Achievement"),
                        ],
                        default="people",
                        max_length=30,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True, verbose_name="Show on homepage")),
            ],
            options={
                "verbose_name": "impact statistic",
                "verbose_name_plural": "impact statistics",
                "ordering": ["order", "label"],
            },
        ),
    ]
