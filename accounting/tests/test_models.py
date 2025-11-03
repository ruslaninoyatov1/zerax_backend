import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from accounting.models import Account,JournalEntry
from datetime import date

User = get_user_model()

class AccountModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gamil.com",
            password="rootroot",
            full_name="TestName",
        )

    # 1. Account modeli uchun qo‘shimcha testlar
    def test_create_account(self):
        account = Account.objects.create(
            user=self.user,
            name="Test Name",
            code = "Test code",
            type = "asset"
        )

        self.assertEqual(account.name,"Test Name")
        self.assertEqual(account.code,"Test code")
        self.assertEqual(account.type,"asset")
        self.assertEqual(account.user,self.user)


    def test_account_code_must_be_unique(self):
        Account.objects.create(user=self.user, name="A", code="1001", type="asset")
        with self.assertRaises(Exception):
            Account.objects.create(user=self.user, name="B", code="1001", type="liability")


    def test_invalid_account_type_raises_error(self):
        account = Account(
            user=self.user,
            name="Invalid Account",
            code="9999",
            type="unknown"  # mavjud bo‘lmagan type
        )
        with self.assertRaises(ValidationError):
            account.full_clean()

    # ==============================================
    # 2. JournalEntry modeli uchun testlar
    # ==============================================

    def test_create_journal_entry(self):
        account = Account.objects.create(
            user=self.user,
            name="Cash",
            code="1001",
            type="asset"
        )
        journal_entry = JournalEntry.objects.create(
            user = self.user,
            account = account,
            debit = 12000,
            credit = 9000,
            date = str(date.today()),
            description = "Test Desc",

        )
        self.assertEqual(journal_entry.debit,12000)
        self.assertEqual(journal_entry.credit,9000)
        self.assertEqual(journal_entry.user,self.user)



    def test_journal_entry_str_method(self):
        account = Account.objects.create(user=self.user, name="Cash", code="1001", type="asset")
        entry = JournalEntry.objects.create(
            user = self.user,
            account=account,
            debit=5000,
            credit=0,
            date=date.today(),
            description="Initial balance"
        )
        expected = f"Journal: {account.name} ({entry.date})"
        self.assertEqual(str(entry), expected)

    def test_journal_entry_raises_error_if_both_zero(self):
        account = Account.objects.create(user=self.user, name="Cash", code="1001", type="asset")
        entry = JournalEntry(
            account=account,
            debit=0,
            credit=0,
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            entry.clean()

    def test_journal_entry_raises_error_if_both_positive(self):
        account = Account.objects.create(user=self.user, name="Cash", code="1001", type="asset")
        entry = JournalEntry(
            account=account,
            debit=1000,
            credit=500,
            date=date.today()
        )
        with self.assertRaises(ValidationError):
            entry.clean()

    def test_journal_entry_valid_entry(self):
        account = Account.objects.create(user=self.user, name="Cash", code="1001", type="asset")
        entry = JournalEntry(
            account=account,
            debit=1000,
            credit=0,
            date=date.today()
        )
        try:
            entry.clean()
        except ValidationError:
            self.fail("ValidationError bo‘lmasligi kerak edi!")

