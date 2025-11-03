import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from settings.models import Integration
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SettingsViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com",
            password="rootroot",
            full_name="Test Name"
        )

        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            password="adminroot",
            full_name="Admin Test Name",
            role="admin"
        )

        self.integration = Integration.objects.create(
            user=self.user,
            provider="click",
            api_key="test_api_key"
        )

        self.integration_url = reverse("integration-list-create")

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_settings_list_authenticated(self):
        """Authenticated foydalanuvchi faqat o‘z Integrationlarini ko‘rishi kerak"""
        self.authenticate(self.user)
        response = self.client.get(self.integration_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['provider'], 'click')

    def test_settings_list_unauthenticated(self):
        """Unauthenticated foydalanuvchi uchun 401 qaytishi kerak"""
        response = self.client.get(self.integration_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_others_integrations(self):
        """Foydalanuvchi faqat o‘z Integrationlarini ko‘rishi kerak"""
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="rootroot",
            full_name="Other User"
        )
        Integration.objects.create(
            user=other_user,
            provider="payme",
            api_key="secret_key"
        )

        self.authenticate(self.user)
        response = self.client.get(self.integration_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['provider'], 'click')

    def test_integration_count_after_multiple_creations(self):
        """Bir foydalanuvchi bir nechta integration yarata olishini tekshiradi"""
        self.authenticate(self.user)
        for i in range(3):
            self.client.post(self.integration_url, {"provider": "click", "api_key": f"key_{i}"}, format='json')

        integrations = Integration.objects.filter(user=self.user)
        self.assertEqual(integrations.count(), 4)  # 1 oldingi + 3 yangi
