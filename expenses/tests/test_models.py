import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from expenses.models import Expense
from datetime import date

User = get_user_model()

class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@gamil.com",
            password="rootroot",
            full_name="Diyorbek",
        )

    def test_create_expense(self):
        expense = Expense.objects.create(
            user = self.user,
            category = "rent",
            amount = 12000,
            date = date.today(),
            note = "Test Note"

        )
        self.assertEqual(expense.category,'rent')
        self.assertEqual(float(expense.amount),12000)
        self.assertEqual(expense.note,'Test Note')
        self.assertEqual(expense.user,self.user)

    def test_expense_str_method(self):
        expense = Expense.objects.create(
            user=self.user,
            category="salary",
            amount=13000,
            date=date.today(),
            note="Test Note"
        )

        expected_str = f"{expense.category} - {expense.amount}"
        self.assertEqual(str(expense), expected_str)

    def test_expense_status_choices(self):

        valid_categories = ['rent', 'salary', 'transport', 'other']

        for category in valid_categories:
            expense = Expense.objects.create(
                user=self.user,
                category=category,
                amount=13000,
                date=date.today(),
                note="Invalid category"
            )
            self.assertIn(expense.category, valid_categories)

    def test_invalid_category_raises_validation_error_on_full_clean(self):
        exp = Expense(user=self.user, category="invalid", amount=10000, date=date.today(), note="Invalid")
        with self.assertRaises(ValidationError):
            exp.full_clean()