import os
import django
from django.conf import settings
if not settings.configured:
    os.environ.setdefault('DJANGO_MODULE_SETTINGS','main.settings')
    django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from settings.models import Integration


User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "user@gamil.com",
            password = "rootroot",
            full_name = 'Test User Name',

        )

    def test_create_user(self):

        self.assertEqual(self.user.email,'user@gamil.com')
        self.assertTrue(self.user.check_password("rootroot"))
        self.assertEqual(self.user.full_name,'Test User Name')


    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email = 'admin@gmail.com',
            password = 'rootroot'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role,'admin')

    def test_str_method(self):
        self.assertEqual(str(self.user),'user@gamil.com')


