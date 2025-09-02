from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import Report
from .serializers import ReportSerializer
from .message import get_message
from rest_framework.parsers import MultiPartParser, FormParser
from costum_permissions.permission import *
# ---- List & Create Reports ----
class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [AdminReadOnly | AccountantReadOnly]
    parser_classes = [MultiPartParser, FormParser]  
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Create a new report",
        request_body=ReportSerializer,
        responses={201: ReportSerializer, 400: "Invalid input"}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save(user=request.user)
        return Response(
            {
                "message": get_message("report_created", request.user),
                "report": ReportSerializer(report).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ---- Export Report ----
class ReportExportView(generics.GenericAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk, user=request.user)
        export_type = request.query_params.get("type", report.export_type)  # default to model

        if export_type not in ["pdf", "excel"]:
            return Response(
                {"error": get_message("invalid_export_type", request.user)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": get_message("export_success", request.user),
                "report_id": report.id,
                "name": report.name,
                "export_type": export_type,
            },
            status=status.HTTP_200_OK,
        )
