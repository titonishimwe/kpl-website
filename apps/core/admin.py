from django.contrib import admin
from .models import MembershipApplication, RoomReservation, Event, BookArrival


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "membership_type",
        "payment_method",
        "phone",
        "status",
        "created_at",
    ]
    list_filter = ["membership_type", "payment_method", "status", "created_at"]
    search_fields = ["first_name", "last_name", "email", "phone", "id_passport"]
    readonly_fields = ["created_at"]


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = [
        "space_type",
        "name",
        "reservation_date",
        "duration",
        "attendees_count",
        "status",
        "created_at",
    ]
    list_filter = ["space_type", "status", "duration", "reservation_date"]
    search_fields = ["name", "email", "phone", "organization", "purpose"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date_text", "location", "is_featured"]
    list_filter = ["is_featured", "event_date"]
    search_fields = ["title", "location", "description"]


@admin.register(BookArrival)
class BookArrivalAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "order"]
    list_filter = ["category"]
    search_fields = ["title"]
