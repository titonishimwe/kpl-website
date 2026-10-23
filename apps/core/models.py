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
    space_type = models.CharField(max_length=100, choices=ROOM_CHOICES)
    reservation_date = models.DateField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default="half_day")
    attendees_count = models.PositiveIntegerField(default=1)
    purpose = models.TextField(help_text="Brief description of the meeting or activity")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
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


class BookArrival(models.Model):
    CATEGORY_CHOICES = [
        ("adult", "Adult"),
        ("teens", "Teens"),
        ("kids", "Kids"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="adult")
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "title"]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
