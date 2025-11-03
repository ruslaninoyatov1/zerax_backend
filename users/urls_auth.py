from django.urls import path
from .views import LoginView, RefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
]