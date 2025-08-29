from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path("api/", include("settings.urls")),
   path("admin/", admin.site.urls),
   path("api/", include("reports.urls")),

   path("api/invoices/",         include("invoices.urls")),
   path("api/auth/register/",     include("users.urls_register")),
   path("api/auth/",              include("users.urls_auth")),     
   path("api/users/",             include("users.urls_me")),       



   path("api/accounting/", include("accounting.urls")),
   path("api/expenses/", include("expenses.urls")),

   path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
   path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)