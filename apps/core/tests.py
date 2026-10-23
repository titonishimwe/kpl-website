from django.test import TestCase
from django.urls import reverse
from .models import MembershipApplication, RoomReservation, Event, BookArrival


class HomePageTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kigali Public Library")
        self.assertContains(response, "Catalog")

    def test_about_page_loads(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who We Are")
        self.assertContains(response, "Vision &amp; Mission")

    def test_careers_page_loads(self):
        response = self.client.get(reverse("core:careers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Careers")

    def test_spaces_pages_load(self):
        res1 = self.client.get(reverse("core:spaces"))
        self.assertEqual(res1.status_code, 200)

        res2 = self.client.get(reverse("core:meeting_rooms"))
        self.assertEqual(res2.status_code, 200)

        res3 = self.client.get(reverse("core:discussion_rooms"))
        self.assertEqual(res3.status_code, 200)

    def test_membership_page_loads(self):
        response = self.client.get(reverse("core:membership"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Get a Library Card")

    def test_membership_submission(self):
        data = {
            "first_name": "Jean",
            "last_name": "Mugisha",
            "dob": "1998-05-15",
            "gender": "male",
            "id_passport": "1199880012345678",
            "phone": "+250788123456",
            "email": "jean@example.com",
            "membership_type": "adult_annual",
            "payment_method": "momo",
            "terms_confirmed": "on",
        }
        response = self.client.post(reverse("core:membership"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MembershipApplication.objects.filter(email="jean@example.com").exists())

    def test_reservation_submission(self):
        data = {
            "name": "Marie Claire",
            "email": "marie@example.com",
            "phone": "+250788654321",
            "organization": "Reading Rwanda",
            "space_type": "Small Meeting Room (4-10 participants)",
            "reservation_date": "2026-11-20",
            "duration": "half_day",
            "attendees_count": 6,
            "purpose": "Author book review and planning session",
        }
        response = self.client.post(reverse("core:reserve_room"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RoomReservation.objects.filter(email="marie@example.com").exists())
