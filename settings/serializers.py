from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Integration

User = get_user_model()


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("language", "theme")  # editable fields only


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = "__all__"
        read_only_fields = ("user",)
