import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError

from reports.models import Report

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class ReportsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@gmail.com",
            password = "rootroot",
            full_name = "TestName"
        )

    def test_create_reports(self):
        reports = Report.objects.create(
            user = self.user,
            name = "TestName",
            source = "invoices",
            filters = {
                'client_name': 'TestName',
                'amount':10000,
            },
            export_type = "excel"
        )
        self.assertEqual(reports.name,'TestName')
        self.assertEqual(reports.source,'invoices')
        self.assertEqual(reports.filters['amount'],10000)
        self.assertEqual(reports.export_type,'excel')
        self.assertEqual(reports.user,self.user)


    def test_str_method(self):
        report = Report.objects.create(
            user=self.user,
            name="Sales Report",
            export_type="excel"
        )
        self.assertEqual(str(report), "Sales Report")

    def test_reports_status_choices(self):

        valid_sources = ['invoices','expenses','accounting']

        for source in valid_sources:
            reports = Report.objects.create(
                user=self.user,
                name="TestName",
                source=source,
                filters={
                    'client_name': 'TestName',
                    'amount': 10000,
                },
                export_type="excel"
            )
            self.assertIn(reports.source,valid_sources)

    def test_invalid_export_type_choice(self):
        report = Report(
            user = self.user,
            name = "Invalid Export",
            export_type = "cvs"
        )
        with self.assertRaises(ValidationError):
            report.full_clean()


    def test_invalid_source_choice(self):
        report = Report.objects.create(
            user = self.user,
            name = "Invalid Source",
            export_type = "pdf",
            source = "random",
        )
        with self.assertRaises(ValidationError):
            report.full_clean()

    def test_file_field_allows_blank_and_null(self):
        report = Report.objects.create(
            user = self.user,
            name="No File Report",
            export_type="pdf",
            file=None
        )
        self.assertIsNotNone(report.file)
        self.assertIsNone(report.file.name)

