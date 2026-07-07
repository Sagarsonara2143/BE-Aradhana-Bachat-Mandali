from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase

from apps.accounts.models import UserRole
from apps.content.models import ContentType, Event, LegalDocument
from apps.enquiries.models import Enquiry
from apps.media_library.models import GalleryCategory, GalleryImage
from apps.plans.models import Plan, PlanTableRow, PlanType

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        cache.clear()  # reset throttle history between tests
        self.admin = User.objects.create_user(
            email="admin@test.com", password="pass12345", role=UserRole.WEBSITE_ADMIN
        )
        self.member = User.objects.create_user(
            email="member@test.com", password="pass12345", role=UserRole.MEMBER
        )
        self.plan = Plan.objects.create(
            name="RD Plan", slug="rd-plan", plan_type=PlanType.RD, is_active=True
        )
        PlanTableRow.objects.create(plan=self.plan, label="6 years", maturity_amount=85140)
        Plan.objects.create(name="Hidden", slug="hidden", plan_type=PlanType.SN, is_active=False)

    def auth(self, user):
        res = self.client.post(
            "/api/v1/auth/login/",
            {"identifier": user.email, "password": "pass12345"},
            format="json",
        )
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class AuthTests(BaseAPITest):
    def test_login_success(self):
        res = self.client.post(
            "/api/v1/auth/login/",
            {"identifier": "admin@test.com", "password": "pass12345"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)

    def test_login_failure(self):
        res = self.client.post(
            "/api/v1/auth/login/",
            {"identifier": "admin@test.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.data["success"])


class PlanTests(BaseAPITest):
    def test_public_list_excludes_inactive(self):
        res = self.client.get("/api/v1/plans/")
        self.assertEqual(res.status_code, 200)
        slugs = [p["slug"] for p in res.data["results"]]
        self.assertIn("rd-plan", slugs)
        self.assertNotIn("hidden", slugs)

    def test_public_detail_has_tables(self):
        res = self.client.get("/api/v1/plans/rd-plan/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["table_rows"]), 1)

    def test_calculator_matches_schedule(self):
        res = self.client.post(
            "/api/v1/plans/calculate/",
            {"plan_type": "RD", "monthly_amount": 1000, "duration_years": 6},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(float(res.data["estimated_maturity"]), 85140.0)
        self.assertIn("disclaimer", res.data)

    def test_admin_create_requires_auth(self):
        res = self.client.post("/api/v1/admin/plans/", {"name": "x"}, format="json")
        self.assertIn(res.status_code, (401, 403))

    def test_admin_create_forbidden_for_member(self):
        self.auth(self.member)
        res = self.client.post("/api/v1/admin/plans/", {"name": "x"}, format="json")
        self.assertEqual(res.status_code, 403)

    def test_admin_create_succeeds(self):
        self.auth(self.admin)
        res = self.client.post(
            "/api/v1/admin/plans/",
            {"name": "New", "slug": "new", "plan_type": "DT"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)


class ContentAndMediaTests(BaseAPITest):
    def test_legal_list(self):
        LegalDocument.objects.create(title="Doc", slug="doc", category="Registration")
        res = self.client.get("/api/v1/legal-documents/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)

    def test_event_list_and_detail(self):
        Event.objects.create(title="AGM", slug="agm", type=ContentType.EVENT)
        self.assertEqual(self.client.get("/api/v1/events/").status_code, 200)
        res = self.client.get("/api/v1/events/agm/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["slug"], "agm")

    def test_gallery_category_filter(self):
        cat = GalleryCategory.objects.create(name="Events", slug="events")
        GalleryImage.objects.create(title="Pic", category=cat, image="gallery/x.jpg")
        res = self.client.get("/api/v1/gallery/images/?category=events")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)


class EnquiryTests(BaseAPITest):
    def test_submit(self):
        res = self.client.post(
            "/api/v1/enquiries/",
            {
                "full_name": "Test",
                "mobile_number": "9898098744",
                "subject": "Hi",
                "message": "Hello there team",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Enquiry.objects.count(), 1)

    def test_admin_can_update_status(self):
        enq = Enquiry.objects.create(
            full_name="A", mobile_number="9999999999", subject="s", message="m"
        )
        self.auth(self.admin)
        res = self.client.patch(
            f"/api/v1/admin/enquiries/{enq.id}/", {"status": "CLOSED"}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        enq.refresh_from_db()
        self.assertEqual(enq.status, "CLOSED")

    def test_public_cannot_list_enquiries(self):
        res = self.client.get("/api/v1/admin/enquiries/")
        self.assertIn(res.status_code, (401, 403))
