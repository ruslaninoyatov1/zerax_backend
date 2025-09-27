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
        title="Zerax API",
        default_version='v1',
        description="Zerax CRM Platform API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@zerax.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth endpoints
    path("api/auth/register/", include("users.urls_register")),
    path("api/auth/", include("users.urls_auth")),
    path("api/users/", include("users.urls_me")),
    path("api/", include("users.urls_admin")),  # Fixed: urls_admin

    # Business logic endpoints
    path("api/", include("settings.urls")),
    path("api/", include("reports.urls")),
    path("api/", include("invoices.urls")),
    path("api/accounting/", include("accounting.urls")),
    path("api/expenses/", include("expenses.urls")),

    # Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # Swagger UI (yasg)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)