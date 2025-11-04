import os
import django
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    django.setup()
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


class RegisterViewTest(APITestCase):

    def test_register_user(self):
        url = reverse("register")
        data = {
            "email": "newuser@gmail.com",
            "password": "rootroot",
            "full_name": "New User",
        }

        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)


class LoginVIewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@gmail.com",
            password = 'rootroot',
            full_name = 'Test Name'
        )

    def test_login_user(self):
        url = reverse('login')
        data = {
            "email": "test@gmail.com",
            "password": "rootroot",
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)

class MyViewTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email = 'me@gmail.com',
            password = 'rootroot',
            full_name = 'Test Name'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_me_retrieve(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['email'],'me@gmail.com')

class UserListCreateViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@gmail.com',
            password='rootroot',
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_list_users_as_admin(self):
        self.authenticate(self.admin)
        url = reverse('user-list-create')

        response = self.client.get(url)
        print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserDetailViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='me@gmail.com',
            password='rootroot',
            full_name='Test Name'
        )

        self.admin = User.objects.create_superuser(
            email='admin@gmail.com',
            password='rootroot'
        )
        self.url = reverse('user-detail', args=[self.user.id])

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_retrieve_user_as_normal_user_forbidden(self):
        self.authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)