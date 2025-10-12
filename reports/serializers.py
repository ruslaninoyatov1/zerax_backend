from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ["id", "user", "name", "source", "filters", "export_type", "file", "file_url", "created_at"]
        read_only_fields = ["id", "user", "created_at", "file_url"]

    def get_file_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if obj.file else None
    # new
    def create(self,validated_data):
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

