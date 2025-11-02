# invoices/tests/test_view.py
import os
from datetime import date

import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from invoices.models import Invoice
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class InvoicesViewSet(APITestCase):
    def setUp(self):
        # normal user
        self.user = User.objects.create_user(
            email="test@gmail.com", password="root1234", full_name="Test User"
        )
        # admin user
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com", password="admin123", full_name="Admin User", role="admin"
        )

        # one invoice for normal user
        self.invoice1 = Invoice.objects.create(
            user=self.user,
            client_name="Test Name",
            amount=10000,
            status="paid",
            due_date=str(date.today()),
        )

        self.invoice_list_url = reverse('invoice-list-create')
        self.invoice_detail_url = reverse('invoice-detail', kwargs={'pk': self.invoice1.pk})

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_invoice_list_authenticated(self):
        """Authenticated foydalanuvchi uchun 200 bo'lishi kerak va faqat uning invoice'lari qaytishi kerak."""
        self.authenticate(self.user)
        response = self.client.get(self.invoice_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # pagination returns results key
        self.assertIn('results', response.data)
        # only owner's invoice should be present
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client_name'], "Test Name")

    def test_invoice_list_unauthenticated(self):
        """Unauthenticated foydalanuvchi uchun 401 bo'lishi kerak (authentication header yo'q)."""
        # NOTE: do not call self.authenticate()
        response = self.client.get(self.invoice_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invoice(self):
        """Authenticated user invoice yaratishi mumkin (201)."""
        self.authenticate(self.user)
        data = {
            "client_name": "New Client",
            "amount": "2000.00",
            "status": "pending",
            "due_date": "2025-12-31"
        }
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('invoice', response.data)
        self.assertEqual(response.data['invoice']['client_name'], "New Client")

    def test_update_invoice(self):
        """Authenticated user invoice o'zgartirish mumkin (200)."""
        self.authenticate(self.user)
        data = {
            "client_name": "New Client",
            "amount": "4000.00",
            "status": "pending",
            "due_date": "2025-12-31"
        }
        response = self.client.put(self.invoice_detail_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete_invoice(self):
        self.authenticate(self.user)
        response = self.client.delete(self.invoice_detail_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('message',response.data)
        self.assertFalse(Invoice.objects.filter(pk=self.invoice1.pk).exists())




    def test_user_can_only_see_own_invoices(self):
        """User faqat o'z invoice'ini ko'rishi kerak; boshqa user invoice'lari ko'rinmasligi kerak."""
        # create invoice for other user
        other_user = User.objects.create_user(email="other@gmail.com", password="root1234", full_name="Other")
        Invoice.objects.create(
            user=other_user,
            client_name="Other Client",
            amount=500,
            status="pending",
            due_date=str(date.today()),
        )

        self.authenticate(self.user)
        response = self.client.get(self.invoice_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # only own invoice present
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client_name'], "Test Name")
