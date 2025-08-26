from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "full_name", "email", "password", "role", "language", "theme")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["language"] = user.language
        token["theme"] = user.theme
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Choose success message based on user language
        messages = {
            "UZ": "Hush kelibsiz",
            "RU": "Добро пожаловать",
            "EN": "Welcome",
        }
        success_message = messages.get(self.user.language, "Welcome")

        data.update({
            "message": success_message,  # add localized message
            "user": {
                "id": self.user.id,
                "email": self.user.email,
                "full_name": self.user.full_name,
                "role": self.user.role,
                "language": self.user.language,
                "theme": self.user.theme,
            }
        })
        return data



class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "role", "language", "theme")
        read_only_fields = ("email", "role")   # adjust as needed
