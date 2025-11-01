from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            return ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("role","admin")
        extra_fields.setdefault("is_staff","True")
        extra_fields.setdefault("is_superuser","True")
        return self.create_user(email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("accountant", "Accountant"),
        ("user", "User"),
    )

    LANGUAGE_CHOICES = [("UZ", "Uzbek"), ("RU", "Russian"), ("EN", "English")]
    THEME_CHOICES = [("light", "Light"), ("dark", "Dark")]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    telegram_id = models.BigIntegerField(unique=True,blank=True,null=True)
    telegram_code = models.CharField(max_length=10, blank=True, null=True)
    web_code = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="EN")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return str(self.email)



class TelegramRegistration(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    site_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tg_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    payload = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TelegramRegistration({self.tg_id})" if self.tg_id else f"TelegramRegistration(pending)"







