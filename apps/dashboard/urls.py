from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),

    path("applications/", views.ApplicationListView.as_view(), name="applications"),
    path("applications/report.pdf", views.ApplicationReportView.as_view(), name="applications_report"),
    path("applications/export.csv", views.ApplicationCsvView.as_view(), name="applications_csv"),
    path("applications/<int:pk>/", views.ApplicationDetailView.as_view(), name="application_detail"),
    path("applications/<int:pk>/pdf/", views.ApplicationPdfView.as_view(), name="application_pdf"),

    path("reservations/", views.ReservationListView.as_view(), name="reservations"),
    path("reservations/report.pdf", views.ReservationReportView.as_view(), name="reservations_report"),
    path("reservations/<int:pk>/", views.ReservationDetailView.as_view(), name="reservation_detail"),

    path("settings/", views.SiteSettingsView.as_view(), name="settings"),

    path("users/", views.UserListView.as_view(), name="users"),
    path("users/<int:pk>/toggle/<str:what>/", views.UserToggleView.as_view(), name="user_toggle"),

    # Events, spaces, staff picks, impact figures, slides, closure days (see resources.py)
    path("content/<slug:slug>/", views.ResourceListView.as_view(), name="resource_list"),
    path("content/<slug:slug>/add/", views.ResourceFormView.as_view(), name="resource_add"),
    path("content/<slug:slug>/<int:pk>/edit/", views.ResourceFormView.as_view(), name="resource_edit"),
    path("content/<slug:slug>/<int:pk>/delete/", views.ResourceDeleteView.as_view(), name="resource_delete"),
]
