import os
from datetime import date
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from expenses.models import Expense
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ExpenseViewSetTest(APITestCase):
    def setUp(self):
        # Asosiy user
        self.user = User.objects.create_user(
            email="user@gmail.com",
            password="rootroot",
            full_name="Diyorbek",
        )

        # Admin user
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            password="rootroot",
            full_name="Admin User",
            role="admin"
        )

        # Bitta expense yozuv
        self.expense = Expense.objects.create(
            user=self.user,
            category="rent",
            amount=12000,
            date=date.today(),
            note="Test Note"
        )

    def authenticate(self, user):
        """JWT token yaratib, so‘rovga header sifatida qo‘shadi"""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    # -------------------------------------------------------
    # TESTLAR
    # -------------------------------------------------------

    def test_expense_list_authenticated(self):
        """✅ Auth bo‘lgan foydalanuvchi o‘z xarajatlarini ko‘radi"""
        self.authenticate(self.user)
        url = reverse("expense-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]["results"]), 1)
        self.assertEqual(response.data["results"]["results"][0]["note"], "Test Note")

    def test_expense_list_unauthenticated(self):
        """🚫 Authsiz foydalanuvchi 401 xatolik oladi"""
        url = reverse("expense-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expense(self):
        """✅ Yangi xarajat yaratish"""
        self.authenticate(self.user)
        url = reverse("expense-list-create")

        data = {
            "category": "salary",
            "amount": 12000,
            "date": str(date.today()),
            "note": "Salary Note"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["expense"]["category"], "salary")

    def test_update_expense(self):
        """✅ Xarajatni yangilash"""
        self.authenticate(self.user)
        url = reverse("expense-detail", kwargs={"pk": self.expense.pk})

        data = {
            "category": "salary",
            "amount": 16000,
            "date": str(date.today()),
            "note": "Updated Note"
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["expense"]["category"], "salary")
        self.assertEqual(response.data["expense"]["note"], "Updated Note")

    def test_delete_expense(self):
        """✅ Xarajatni o‘chirish"""
        self.authenticate(self.user)
        url = reverse("expense-detail", kwargs={"pk": self.expense.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())

    def test_user_can_only_see_own_expenses(self):
        """✅ Har bir user faqat o‘z yozuvlarini ko‘radi"""
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="rootroot",
            full_name="Another User",
            telegram_id=1954153232
        )

        Expense.objects.create(
            user=other_user,
            category="other",
            amount=9999,
            date=date.today(),
            note="Not visible note"
        )

        self.authenticate(self.user)
        url = reverse("expense-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]["results"]), 1)
        self.assertEqual(response.data["results"]["results"][0]["user"], self.user.id)
