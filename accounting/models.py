from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Account(models.Model):
    TYPE_CHOICES = [
        ("asset","Asset"),
        ("liability","Liability"),
        ("equity","Equity"),
        ("income","Income"),
        ("expense","Expense"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES,default="asset")

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journal_entries")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="journal_entries")
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal: {self.account.name} ({self.date})"

    def clean(self):
        if self.debit <= 0 and self.credit <= 0:
            raise ValidationError("Debit yoki Credit qiymatlaridan biri musbat bo‘lishi kerak.")
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("Bir vaqtning o‘zida Debit va Credit kiritilmasligi kerak.")