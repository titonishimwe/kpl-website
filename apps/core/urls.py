from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("careers/", views.careers, name="careers"),
    path("privacy/", views.privacy, name="privacy"),
    path("spaces/", views.spaces_overview, name="spaces"),
    path("spaces/meeting-rooms/", views.meeting_rooms, name="meeting_rooms"),
    path("spaces/discussion-rooms/", views.discussion_rooms, name="discussion_rooms"),
    path("spaces/reserve/", views.reserve_room, name="reserve_room"),
    path("membership/", views.membership, name="membership"),
    path("events/", views.events_view, name="events"),
]
