from django.contrib import admin
from .models import MembershipApplication, RoomReservation, Event, StaffPick, ImpactStat, SiteSettings, Space, HomeSlide, ClosedDay


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


@admin.register(StaffPick)
class StaffPickAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "recommended_by", "is_active", "added_on", "order"]
    list_editable = ["is_active", "order"]
    list_filter = ["is_active", "category", "added_on"]
    search_fields = ["title", "author", "recommended_by"]


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ["value", "label", "icon", "is_active", "order"]
    list_editable = ["is_active", "order"]


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "capacity_label", "is_active", "order"]
    list_editable = ["is_active", "order"]
    list_filter = ["category", "is_active"]


@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "order"]
    list_editable = ["is_active", "order"]


@admin.register(ClosedDay)
class ClosedDayAdmin(admin.ModelAdmin):
    list_display = ["date", "reason"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
