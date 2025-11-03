from django.urls import path
from .views import SettingsView, IntegrationListCreateView

urlpatterns = [
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/integrations/", IntegrationListCreateView.as_view(), name="integration-list-create"),
]
