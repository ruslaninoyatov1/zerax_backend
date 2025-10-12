from django.db import models
from django.conf import settings

class Report(models.Model):
    EXPORT_TYPE_CHOICES = [
        ("excel", "Excel"),
        ("pdf", "PDF"),
    ]
    # New opt
    SOURCE_CHOICES = [
        ('invoices','Invoices'),
        ('expenses','Expenses'),
        ('accounting','Accounting')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports"
    )
    name = models.CharField(max_length=255)
    filters = models.JSONField(blank=True, null=True)
    source = models.CharField(max_length=20,choices=SOURCE_CHOICES,default='invoices')
    export_type = models.CharField(max_length=10, choices=EXPORT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)



    file = models.FileField(
        upload_to="reports/",   # Files will be stored under MEDIA_ROOT/reports/
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
