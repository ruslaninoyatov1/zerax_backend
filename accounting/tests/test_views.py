# accounting/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from users.models import User
from accounting.models import Account, JournalEntry


class AccountingViewSetTest(APITestCase):
    def setUp(self):
        # ---- Foydalanuvchilar yaratamiz ----
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="admin123",
            role="admin"
        )
        self.accountant_user = User.objects.create_user(
            email="acc@example.com",
            password="acc123",
            role="accountant"
        )

        # API clientlar
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin_user)

        self.client_acc = APIClient()
        self.client_acc.force_authenticate(user=self.accountant_user)

        # Asosiy URLlar
        self.account_url = reverse("account-list-create")
        self.journal_url = reverse("journal-list-create")
        self.balance_url = reverse("balance-sheet")

    # ---- Account yaratish testi ----
    def test_create_account_by_admin(self):
        data = {
            "name": "Test Account",
            "code": "A100",
            "type": "asset"
        }
        response = self.client_admin.post(self.account_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)

    # ---- Accountant foydalanuvchi account yarata oladi ----
    def test_create_account_by_accountant(self):
        data = {
            "name": "Cash",
            "code": "CASH01",
            "type": "asset"
        }
        response = self.client_acc.post(self.account_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Account.objects.filter(code="CASH01").exists())

    # ---- Account ro‘yxatini olish ----
    def test_get_accounts_list(self):
        Account.objects.create(user=self.admin_user, name="Bank", code="B001", type="asset")
        response = self.client_admin.get(self.account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    # ---- Journal entry yaratish ----
    def test_create_journal_entry(self):
        account = Account.objects.create(user=self.admin_user, name="Sales", code="S001", type="income")
        data = {
            "account": account.id,
            "debit": "0.00",
            "credit": "2000.00",
            "date": timezone.now().date(),
            "description": "Income from sales"
        }
        response = self.client_admin.post(self.journal_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JournalEntry.objects.count(), 1)

    # ---- Balance sheet test ----
    def test_balance_sheet_view(self):
        account = Account.objects.create(user=self.admin_user, name="Cash", code="C001", type="asset")
        JournalEntry.objects.create(
            user=self.admin_user,
            account=account,
            debit=1000,
            credit=0,
            description="Initial capital",
            date=timezone.now().date()
        )
        response = self.client_admin.get(self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("balance_sheet", response.data)
        self.assertIn("asset", response.data["balance_sheet"])

    # ---- Filter va search testlari ----
    def test_journal_entry_filter_search(self):
        account = Account.objects.create(user=self.admin_user, name="Cash", code="C002", type="asset")
        JournalEntry.objects.create(
            user=self.admin_user,
            account=account,
            debit=500,
            credit=0,
            date=timezone.now().date(),
            description="Test Filter"
        )
        # Search orqali izlash
        response = self.client_admin.get(f"{self.journal_url}?search=Filter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Filter" in entry["description"] for entry in response.data))
