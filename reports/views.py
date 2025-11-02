from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Report
from .serializers import ReportSerializer
from .message import get_message
from custom_permissions.permission import *
from core.utils.export import generate_report_file
from django.conf import settings

# Update
class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    parser_classes = [MultiPartParser, FormParser,JSONParser]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Report.objects.none()
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

        # Fayl generatsiyasini darhol ishga tushirish
        try:
            file_path = generate_report_file(report, report.export_type)
            if file_path:
                # Serializer bilan yangilangan report ni qaytarish
                updated_report = Report.objects.get(id=report.id)
                response_serializer = ReportSerializer(updated_report, context={'request': request})

                return Response(
                    {
                        "message": get_message("report_created", request.user),
                        "report": response_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                # Agar fayl yaratishda xatolik bo'lsa
                return Response(
                    {
                        "message": get_message("report_created_but_export_failed", request.user),
                        "report": ReportSerializer(report, context={'request': request}).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            print(f"Error in create view: {e}")
            return Response(
                {
                    "message": f"Report created but export failed: {str(e)}",
                    "report": ReportSerializer(report, context={'request': request}).data,
                },
                status=status.HTTP_201_CREATED,
            )

# Update
class ReportExportView(generics.GenericAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk, user=request.user)
        export_type = request.query_params.get("type", report.export_type)

        if export_type not in ["pdf", "excel"]:
            return Response(
                {"error": get_message("invalid_export_type", request.user)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_path = generate_report_file(report, export_type)

        if not file_path:
            return Response(
                {"error": get_message("export_failed", request.user)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Report ni yangilash
        report.refresh_from_db()

        return Response(
            {
                "message": get_message("export_success", request.user),
                "report": ReportSerializer(report, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )

