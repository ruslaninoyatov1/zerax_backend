from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "user", "name", "filters", "export_type", "file", "created_at"]
        read_only_fields = ["id", "user", "created_at"]