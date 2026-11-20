from django.db import migrations

# The rooms that were hard-coded in views.py and the booking form before spaces became editable.
SPACES = [
    ("Small Meeting Room", "meeting", "4–10 participants",
     "Suitable for interviews, consultations, private meetings, and focused discussions.", 1),
    ("Medium Meeting Room", "meeting", "10–25 participants",
     "Designed for workshops, training sessions, collaborative meetings, and professional engagements.", 2),
    ("Large Meeting Room", "meeting", "25–50 participants",
     "Ideal for presentations, stakeholder meetings, board sessions, and larger group discussions.", 3),
    ("Grey Discussion Room", "discussion", "Up to 4 participants",
     "Air-conditioned, equipped with whiteboards and high-speed Wi-Fi.", 1),
    ("Blue Discussion Room", "discussion", "Up to 4 participants",
     "Air-conditioned, equipped with whiteboards and high-speed Wi-Fi.", 2),
    ("Red Discussion Room", "discussion", "Up to 4 participants",
     "Air-conditioned, equipped with whiteboards and high-speed Wi-Fi.", 3),
    ("Event Space / Amphitheater", "event", "",
     "Versatile venue for conferences, public talks, book launches, exhibitions, and community events.", 1),
]


def seed(apps, schema_editor):
    Space = apps.get_model("core", "Space")
    if Space.objects.exists():
        return
    for name, category, capacity, description, order in SPACES:
        rates = {"half_day_rate": "5,000 RWF", "full_day_rate": "10,000 RWF"} if category == "discussion" else {}
        Space.objects.create(
            name=name, category=category, capacity_label=capacity,
            description=description, order=order, **rates,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_dashboard_content"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
