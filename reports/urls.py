from django.urls import path
from .views import ReportListCreateView, ReportExportView

urlpatterns = [
    path("reports/", ReportListCreateView.as_view(), name="report-list-create"),
    path("reports/<int:pk>/export/", ReportExportView.as_view(), name="report-export"),
]
