from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.core.models import (
    ClosedDay, Event, MembershipApplication, RoomReservation, SiteSettings, Space, StaffPick,
)

User = get_user_model()


def make_application(**kwargs):
    data = dict(
        first_name="Jean", last_name="Mugisha", dob=date(1998, 5, 15), gender="male",
        id_passport="1199880012345678", phone="+250788123456", email="jean@example.com",
        district="Gasabo", membership_type="adult_annual",
    )
    data.update(kwargs)
    return MembershipApplication.objects.create(**data)


class AccessTest(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=/dashboard/", fetch_redirect_response=False)

    def test_regular_user_forbidden(self):
        User.objects.create_user("reader", password="pw-123456!")
        self.client.login(username="reader", password="pw-123456!")
        self.assertEqual(self.client.get(reverse("dashboard:home")).status_code, 403)

    def test_staff_cannot_manage_users(self):
        User.objects.create_user("staff", password="pw-123456!", is_staff=True)
        self.client.login(username="staff", password="pw-123456!")
        self.assertEqual(self.client.get(reverse("dashboard:home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("dashboard:users")).status_code, 403)

    def test_staff_login_lands_on_dashboard(self):
        User.objects.create_user("staff", password="pw-123456!", is_staff=True)
        response = self.client.post(reverse("accounts:login"), {"username": "staff", "password": "pw-123456!"})
        self.assertRedirects(response, reverse("dashboard:home"), fetch_redirect_response=False)

    def test_login_ignores_offsite_next(self):
        User.objects.create_user("reader", password="pw-123456!")
        response = self.client.post(
            reverse("accounts:login") + "?next=https://evil.example.com/",
            {"username": "reader", "password": "pw-123456!"},
        )
        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)


class StaffDashboardTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("david", "david@example.com", "pw-123456!")
        self.client.login(username="david", password="pw-123456!")

    def test_every_page_renders(self):
        app = make_application()
        res = RoomReservation.objects.create(
            name="Marie", email="m@example.com", phone="1", space_type="Grey Discussion Room (Up to 4 participants)",
            reservation_date=timezone.localdate() + timedelta(days=3), purpose="Study",
        )
        urls = [
            reverse("dashboard:home"),
            reverse("dashboard:applications"),
            reverse("dashboard:application_detail", args=[app.pk]),
            reverse("dashboard:reservations"),
            reverse("dashboard:reservation_detail", args=[res.pk]),
            reverse("dashboard:settings"),
            reverse("dashboard:users"),
        ]
        for slug in ["events", "spaces", "staff-picks", "impact", "slides", "closures"]:
            urls += [reverse("dashboard:resource_list", args=[slug]), reverse("dashboard:resource_add", args=[slug])]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_approve_application_records_reviewer(self):
        app = make_application()
        self.client.post(reverse("dashboard:application_detail", args=[app.pk]), {"quick_status": "approved"})
        app.refresh_from_db()
        self.assertEqual(app.status, "approved")
        self.assertEqual(app.reviewed_by, self.admin)
        self.assertIsNotNone(app.reviewed_at)

    def test_bulk_reject(self):
        a, b = make_application(), make_application(email="b@example.com")
        self.client.post(reverse("dashboard:applications"), {"bulk_status": "rejected", "selected": [a.pk, b.pk]})
        self.assertEqual(MembershipApplication.objects.filter(status="rejected").count(), 2)

    def test_filters_narrow_the_list(self):
        make_application(first_name="Alice", status="approved")
        make_application(first_name="Bob")
        response = self.client.get(reverse("dashboard:applications") + "?status=pending")
        self.assertContains(response, "Bob")
        self.assertNotContains(response, "Alice")

    def test_pdf_reports(self):
        app = make_application(first_name="Aimée")  # accented name must not break the PDF
        for url in [
            reverse("dashboard:applications_report") + "?status=pending",
            reverse("dashboard:application_pdf", args=[app.pk]),
            reverse("dashboard:reservations_report"),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Content-Type"], "application/pdf")
                self.assertTrue(response.content.startswith(b"%PDF"))

    def test_csv_export(self):
        make_application()
        response = self.client.get(reverse("dashboard:applications_csv"))
        self.assertIn("Mugisha", response.content.decode("utf-8-sig"))

    def test_create_event_shows_on_site(self):
        self.client.post(reverse("dashboard:resource_add", args=["events"]), {
            "title": "Poetry Evening", "event_date": (timezone.localdate() + timedelta(days=5)).isoformat(),
            "date_text": "Friday, 6 p.m.", "location": "Amphitheater", "link": "", "description": "",
        })
        self.assertTrue(Event.objects.filter(title="Poetry Evening").exists())
        self.assertContains(self.client.get(reverse("core:events")), "Poetry Evening")

    def test_disabling_space_removes_it_from_booking_form(self):
        space = Space.objects.get(name="Red Discussion Room")
        response = self.client.get(reverse("dashboard:resource_edit", args=["spaces", space.pk]))
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse("dashboard:resource_edit", args=["spaces", space.pk]), {
            "name": space.name, "category": space.category, "capacity_label": space.capacity_label,
            "description": space.description, "half_day_rate": "", "full_day_rate": "", "order": 3,
            # is_active unticked
        })
        space.refresh_from_db()
        self.assertFalse(space.is_active)
        self.assertNotContains(self.client.get(reverse("core:reserve_room")), 'value="Red Discussion Room')

    def test_delete_staff_pick(self):
        pick = StaffPick.objects.create(title="Old Pick")
        self.client.post(reverse("dashboard:resource_delete", args=["staff-picks", pick.pk]))
        self.assertFalse(StaffPick.objects.filter(pk=pick.pk).exists())

    def test_settings_update_contact_details_on_site(self):
        data = {
            "hero_title": "Welcome to KPL", "hero_subtitle": "Sub", "announcement": "Closed on Monday",
            "phone": "+250 700 000 000", "email": "hello@kplonline.org", "address_line1": "KN 8 Ave",
            "address_line2": "Kigali", "map_url": "", "recruitment_email": "jobs@kplonline.org",
            "weekday_open": "09:00", "weekday_close": "18:00", "weekend_open": "10:00", "weekend_close": "16:00",
            "facebook_url": "", "instagram_url": "", "x_url": "", "youtube_url": "",
        }
        response = self.client.post(reverse("dashboard:settings"), data)
        self.assertRedirects(response, reverse("dashboard:settings"))
        page = self.client.get(reverse("core:home"))
        self.assertContains(page, "Welcome to KPL")
        self.assertContains(page, "+250 700 000 000")
        self.assertContains(page, "9:00 AM – 6:00 PM")
        self.assertContains(page, "Closed on Monday")

    def test_settings_reject_closing_before_opening(self):
        settings = SiteSettings.load()
        response = self.client.post(reverse("dashboard:settings"), {
            "hero_title": "x", "hero_subtitle": "x", "phone": "1", "email": "a@b.co", "address_line1": "a",
            "address_line2": "b", "recruitment_email": "a@b.co",
            "weekday_open": "18:00", "weekday_close": "09:00", "weekend_open": "08:00", "weekend_close": "17:00",
        })
        self.assertContains(response, "Closing time must be after opening time.")
        settings.refresh_from_db()
        self.assertEqual(settings.weekday_close.hour, 20)

    def test_closure_day_marks_library_closed(self):
        ClosedDay.objects.create(date=timezone.localdate(), reason="Umuganda")
        self.assertContains(self.client.get(reverse("core:home")), "Closed today: Umuganda")

    def test_superuser_grants_staff_access(self):
        reader = User.objects.create_user("reader", password="pw-123456!")
        self.client.post(reverse("dashboard:user_toggle", args=[reader.pk, "staff"]))
        reader.refresh_from_db()
        self.assertTrue(reader.is_staff)

    def test_cannot_lock_yourself_out(self):
        self.client.post(reverse("dashboard:user_toggle", args=[self.admin.pk, "active"]))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)
