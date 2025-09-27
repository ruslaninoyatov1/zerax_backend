import os
import django
from django.conf import settings

# Django settings ni configure qilish
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from invoices.models import Invoice
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class InvoicesViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="root1234",
            full_name="Test User"
        )
        self.admin_user = User.objects.create_user(
            email="admin@email.com",
            password="root12345",
            full_name="Admin User",
            role="admin"
        )

        self.invoice1 = Invoice.objects.create(
            user=self.user,
            client_name="Test_name",
            amount=1000,
            status="paid",
            due_date="2025-09-12"
        )

    def test_invoice_list_authenticated(self):
        """Test invoice list with authenticated user"""
        url = reverse("invoice-list-create")

        # JWT token bilan authenticate qilish
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client_name'], "Test_name")

    def test_invoice_list_unauthenticated(self):
        """Test invoice list without authentication"""
        url = reverse("invoice-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invoice(self):
        """Test creating new invoice"""
        url = reverse("invoice-list-create")

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = {
            "client_name": "New Client",
            "amount": 2000.00,
            "status": "pending",
            "due_date": "2025-12-31"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["invoice"]["client_name"], "New Client")

    def test_invoice_detail_view(self):
        """Test invoice detail view"""
        url = reverse("invoice-detail", kwargs={"pk": self.invoice1.pk})

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["client_name"], "Test_name")

    def test_update_invoice(self):
        """Test updating invoice"""
        url = reverse("invoice-detail", kwargs={"pk": self.invoice1.pk})

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = {
            "client_name": "Updated Client",
            "amount": 1500.00,
            "status": "paid"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["invoice"]["client_name"], "Updated Client")

    def test_delete_invoice(self):
        """Test deleting invoice"""
        url = reverse("invoice-detail", kwargs={"pk": self.invoice1.pk})

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        # Invoice o'chirilganini tekshirish
        self.assertFalse(Invoice.objects.filter(pk=self.invoice1.pk).exists())

    def test_user_can_only_see_own_invoices(self):
        """Test that users can only see their own invoices"""
        # Boshqa user yaratish
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="root1234",
            full_name="Other User"
        )

        # Boshqa userga invoice yaratish
        Invoice.objects.create(
            user=other_user,
            client_name="Other Client",
            amount=500,
            status="pending",
            due_date="2025-10-10"
        )

        url = reverse("invoice-list-create")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Faqat o'z invoice'ini ko'rishi kerak
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client_name'], "Test_name")