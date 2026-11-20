import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone


class MembershipApplication(models.Model):
    MEMBERSHIP_CHOICES = [
        ("children_annual", "Children Annual (7,500 RWF)"),
        ("student_monthly", "Student Monthly (1,500 RWF)"),
        ("student_annual", "Student Annual (12,000 RWF)"),
        ("adult_monthly", "Adult Monthly (2,500 RWF)"),
        ("adult_annual", "Adult Annual (20,000 RWF)"),
        ("internet_monthly", "Internet Café Monthly (10,000 RWF)"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    PAYMENT_CHOICES = [
        ("momo", "MoMo Pay (*182*8*1*021216#)"),
        ("card", "Bank Card"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    id_passport = models.CharField(max_length=100, verbose_name="National ID / Passport")

    phone = models.CharField(max_length=50)
    alt_phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    alt_email = models.EmailField(blank=True)

    village = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)

    # Guardian details (if applicant is minor under 18)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_relationship = models.CharField(max_length=100, blank=True)
    guardian_id = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=50, blank=True)

    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="momo")
    document = models.FileField(upload_to="documents/membership/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    staff_notes = models.TextField(blank=True, help_text="Internal notes, never shown to the applicant.")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_membership_type_display()})"


class RoomReservation(models.Model):
    ROOM_CHOICES = [
        ("Small Meeting Room (4-10 participants)", "Small Meeting Room (4-10 participants)"),
        ("Medium Meeting Room (10-25 participants)", "Medium Meeting Room (10-25 participants)"),
        ("Large Meeting Room (25-50 participants)", "Large Meeting Room (25-50 participants)"),
        ("Grey Discussion Room (up to 4 participants)", "Grey Discussion Room (up to 4 participants)"),
        ("Blue Discussion Room (up to 4 participants)", "Blue Discussion Room (up to 4 participants)"),
        ("Red Discussion Room (up to 4 participants)", "Red Discussion Room (up to 4 participants)"),
        ("Event Space / Amphitheater", "Event Space / Amphitheater"),
    ]

    DURATION_CHOICES = [
        ("half_day", "Half Day"),
        ("full_day", "Full Day"),
        ("custom", "Custom Hours"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    organization = models.CharField(max_length=150, blank=True)
    # Stores the space's booking label. Choices come from active Space rows (see RoomReservationForm).
    space_type = models.CharField(max_length=150)
    reservation_date = models.DateField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default="half_day")
    attendees_count = models.PositiveIntegerField(default=1)
    purpose = models.TextField(help_text="Brief description of the meeting or activity")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    staff_notes = models.TextField(blank=True, help_text="Internal notes, never shown to the applicant.")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-reservation_date", "-created_at"]

    def __str__(self):
        return f"{self.space_type} - {self.name} on {self.reservation_date}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_text = models.CharField(max_length=100, help_text="e.g. November 14, 9:30–9:50 a.m.")
    event_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=150)
    link = models.URLField(blank=True, default="#")
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["event_date", "title"]

    def __str__(self):
        return self.title


class StaffPick(models.Model):
    """A book recommended by the KPL team, shown in the homepage Staff Picks section.

    Staff refresh the list every two weeks: untick "Show on homepage" for old picks
    and add new ones, so earlier recommendations stay on record.
    """

    CATEGORY_CHOICES = [
        ("adult", "Adult"),
        ("teens", "Teens"),
        ("kids", "Kids"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="adult")
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    recommended_by = models.CharField(
        max_length=100, blank=True, help_text="Staff member's first name, e.g. 'Aline, Children's Librarian'"
    )
    note = models.CharField(
        max_length=240, blank=True, help_text="One or two sentences on why the team recommends this book."
    )
    is_active = models.BooleanField("Show on homepage", default=True)
    order = models.PositiveIntegerField(default=0)
    added_on = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["category", "order", "title"]
        verbose_name = "staff pick"
        verbose_name_plural = "staff picks"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class ImpactStat(models.Model):
    """A headline figure for the homepage "Our Impact" section."""

    ICON_CHOICES = [
        ("people", "Visitors"),
        ("person-vcard", "Members"),
        ("book", "Books"),
        ("laptop", "Digital resources"),
        ("emoji-smile", "Children & youth"),
        ("calendar-event", "Events"),
        ("building", "Libraries"),
        ("award", "Achievement"),
    ]

    value = models.CharField(max_length=30, help_text="As it should appear, e.g. '120,000+' or '3.5K'")
    label = models.CharField(max_length=80, help_text="e.g. 'Library visitors in 2025'")
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default="people")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField("Show on homepage", default=True)

    class Meta:
        ordering = ["order", "label"]
        verbose_name = "impact statistic"
        verbose_name_plural = "impact statistics"

    def __str__(self):
        return f"{self.value} {self.label}"


class SiteSettings(models.Model):
    """Site-wide content staff edit from the dashboard. There is only ever one row (pk=1)."""

    hero_title = models.CharField("Cover headline", max_length=120, default="Read. Learn. Discover.")
    hero_subtitle = models.CharField(
        "Cover text",
        max_length=255,
        default="An open space for every reader in Kigali: books, digital resources, study spaces and programs for all ages.",
    )
    hero_image = models.ImageField(
        "Cover photo",
        upload_to="site/", blank=True, null=True,
        help_text="Homepage cover photo. Use a wide landscape photo, at least 2000px wide.",
    )
    announcement = models.CharField(
        max_length=255, blank=True,
        help_text="Optional notice shown in a bar at the top of every page, e.g. a holiday closure.",
    )

    phone = models.CharField(max_length=50, default="+250 788 500 777")
    email = models.EmailField(default="info@kplonline.org")
    address_line1 = models.CharField("Address line 1", max_length=150, default="KN 8 Avenue, Gasabo")
    address_line2 = models.CharField("Address line 2", max_length=150, default="Kigali, Rwanda")
    map_url = models.URLField("Google Maps link", blank=True, default="https://maps.app.goo.gl/ZjdB5MHwKms4dHMC9")
    recruitment_email = models.EmailField(default="recruitment@kplonline.org")

    weekday_open = models.TimeField("Monday–Friday opens", default=datetime.time(8, 0))
    weekday_close = models.TimeField("Monday–Friday closes", default=datetime.time(20, 0))
    weekend_open = models.TimeField("Saturday–Sunday opens", default=datetime.time(8, 0))
    weekend_close = models.TimeField("Saturday–Sunday closes", default=datetime.time(17, 0))

    facebook_url = models.URLField(blank=True, default="https://facebook.com/kigalipubliclibrary")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/kigalipubliclibrary")
    x_url = models.URLField("X (Twitter) URL", blank=True, default="https://twitter.com/kigalilibrary")
    youtube_url = models.URLField(blank=True, default="https://youtube.com/@kigalipubliclibrary")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def phone_link(self):
        return "".join(ch for ch in self.phone if ch.isdigit() or ch == "+")


class Space(models.Model):
    """A bookable room or venue. Active spaces appear on the public pages and in the booking form."""

    CATEGORY_CHOICES = [
        ("meeting", "Meeting room"),
        ("discussion", "Discussion room"),
        ("event", "Event space"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    capacity_label = models.CharField(max_length=60, blank=True, help_text="e.g. '10–25 participants'")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="spaces/", blank=True, null=True)
    half_day_rate = models.CharField(max_length=40, blank=True, help_text="e.g. '5,000 RWF'")
    full_day_rate = models.CharField(max_length=40, blank=True, help_text="e.g. '10,000 RWF'")
    is_active = models.BooleanField("Available for booking", default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name

    @property
    def booking_label(self):
        """Text stored on reservations, e.g. 'Small Meeting Room (4–10 participants)'."""
        return f"{self.name} ({self.capacity_label})" if self.capacity_label else self.name

    # Names the public room templates use.
    @property
    def title(self):
        return self.name

    @property
    def capacity(self):
        return self.capacity_label


class HomeSlide(models.Model):
    """A slide in the homepage "What's Happening at the Library" carousel."""

    title = models.CharField(max_length=120)
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="slides/")
    link = models.URLField(blank=True)
    is_active = models.BooleanField("Show on homepage", default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ClosedDay(models.Model):
    """A date the library is closed (public holiday, maintenance). Drives the open/closed badge."""

    date = models.DateField(unique=True)
    reason = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date:%d %b %Y} {self.reason}".strip()
