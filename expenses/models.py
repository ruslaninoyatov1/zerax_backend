from django.db import models
from django.conf import settings
from company.menagers import CompanyManager
from company.models import Company

class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="expenses")

    CATEGORY_CHOICES = [
        ("rent", "Rent"),
        ("salary", "Salary"),
        ("transport", "Transport"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CompanyManager() 
    def __str__(self):
        return f"{self.category} - {self.amount}"
