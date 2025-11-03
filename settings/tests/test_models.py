import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from settings.models import Integration
from datetime import datetime

User = get_user_model()

class IntegrationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="rootroot",
            full_name="TestName",
        )

    def test_integration_create(self):
        integration = Integration.objects.create(
            user=self.user,
            provider="click",
            api_key="test_api_key"
        )
        self.assertEqual(integration.provider, "click")
        self.assertEqual(integration.api_key, "test_api_key")
        self.assertEqual(integration.user, self.user)

    def test_str_method(self):
        integration = Integration.objects.create(
            user=self.user,
            provider="click",
            api_key="test_api_key"
        )
        expected_str = f"{integration.provider} - {self.user.email}"
        self.assertEqual(str(integration), expected_str)

    def test_created_at_auto_now_add(self):
        integration = Integration.objects.create(
            user=self.user,
            provider="click",
            api_key="auto_key"
        )
        self.assertIsNotNone(integration.created_at)
        self.assertIsInstance(integration.created_at, datetime)

    def test_invalid_provider_choice(self):
        from django.core.exceptions import ValidationError

        integration = Integration(
            user=self.user,
            provider="unknown",
            api_key="bad_key"
        )
        with self.assertRaises(ValidationError):
            integration.full_clean()
            integration.save()

    def test_multiple_integrations_per_user(self):
        Integration.objects.create(user=self.user, provider="click", api_key="key1")
        Integration.objects.create(user=self.user, provider="payme", api_key="key2")
        self.assertEqual(self.user.integrations.count(), 2)
