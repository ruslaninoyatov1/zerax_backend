import os
import django
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from reports.models import Report

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    django.setup()

User = get_user_model()


class ReportsViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@gmail.com",
            password="rootroot",
            full_name="UserTest"
        )

        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            password="root1234",
            full_name="AdminTest",
            role="admin"
        )

        self.report1 = Report.objects.create(
            user=self.user,
            name="First Report",
            filters={"client_name": "Ali", "amount": 5000},
            source="invoices",
            export_type="pdf"
        )

    # JWT orqali autentifikatsiya
    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    # 1 GET /api/reports/
    def test_get_reports_list_authenticated(self):
        self.authenticate(self.user)
        url = reverse('report-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_reports_list_unauthorized(self):
        url = reverse('report-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 2 POST /api/reports/
    def test_create_report(self):
        self.authenticate(self.user)
        url = reverse("report-list-create")

        data = {
            "name": "New Test Report",
            "filters": {"client_name": "Hasan", "amount": 10000},
            "source": "invoices",
            "export_type": "excel"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["report"]["source"], "invoices")

    def test_create_invalid_report(self):
        self.authenticate(self.user)
        url = reverse("report-list-create")

        data = {
            "name": "",
            "filters": {},
            "source": "invoices",
            "export_type": "pdf"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 3 GET /api/reports/{id}/export?type=pdf
    def test_export_report_pdf(self):
        self.authenticate(self.user)
        url = reverse("report-export", kwargs={"pk": self.report1.pk})
        response = self.client.get(f"{url}?type=pdf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("report", response.data)

    def test_export_report_not_found(self):
        self.authenticate(self.user)
        url = reverse("report-export", kwargs={"pk": 9999})
        response = self.client.get(f"{url}?type=pdf")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
