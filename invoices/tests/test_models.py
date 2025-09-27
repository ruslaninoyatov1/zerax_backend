import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from invoices.models import Invoice
from datetime import date

User = get_user_model()


class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            full_name="Test User"
        )

    def test_create_invoice(self):
        """Test invoice creation"""
        invoice = Invoice.objects.create(
            user=self.user,
            client_name="Test Client",
            amount=1500.00,
            status="pending",
            due_date=date.today()
        )

        self.assertEqual(invoice.client_name, "Test Client")
        self.assertEqual(float(invoice.amount), 1500.00)
        self.assertEqual(invoice.status, "pending")
        self.assertEqual(invoice.user, self.user)

    def test_invoice_str_method(self):
        """Test invoice string representation"""
        invoice = Invoice.objects.create(
            user=self.user,
            client_name="Test Client",
            amount=1500.00,
            status="pending",
            due_date=date.today()
        )

        expected_str = f"Invoice {invoice.id} - Test Client"
        self.assertEqual(str(invoice), expected_str)

    def test_invoice_status_choices(self):
        """Test invoice status choices"""
        valid_statuses = ["paid", "unpaid", "pending"]

        for status in valid_statuses:
            invoice = Invoice.objects.create(
                user=self.user,
                client_name=f"Client {status}",
                amount=1000.00,
                status=status,
                due_date=date.today()
            )
            self.assertEqual(invoice.status, status)