from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Integration
from .serializers import IntegrationSerializer, UserSettingsSerializer
from .message import get_message
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


# ---- User Settings (GET, PUT) ----
class SettingsView(generics.RetrieveUpdateAPIView):
    """
    GET /api/settings/ – umumiy sozlamalar
    PUT /api/settings/ – til, theme o‘zgartirish
    """
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={200: UserSettingsSerializer()}
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(
            {
                "message": get_message("settings_retrieved", request.user),
                "settings": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=UserSettingsSerializer,
        responses={200: UserSettingsSerializer()}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)  # allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": get_message("settings_updated", request.user),
                "settings": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ---- Create Integration ----
class IntegrationCreateView(generics.CreateAPIView):
    """
    POST /api/settings/integrations/ – to‘lov integratsiyasi qo‘shish
    """
    serializer_class = IntegrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=IntegrationSerializer,
        responses={201: IntegrationSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        integration = serializer.save(user=request.user)
        return Response(
            {
                "message": get_message("integration_created", request.user),
                "integration": IntegrationSerializer(integration).data,
            },
            status=status.HTTP_201_CREATED,
        )
