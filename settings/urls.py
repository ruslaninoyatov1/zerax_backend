from django.urls import path
from .views import SettingsView, IntegrationCreateView

urlpatterns = [
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/integrations/", IntegrationCreateView.as_view(), name="integration-create"),
]
