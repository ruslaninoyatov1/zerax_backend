from django.db import models

class Account(models.Model):
    TYPE_CHOICES = [
        ("asset","Asset"),
        ("liability","Liability"),
        ("equity","Equity"),
        ("income","Income"),
        ("expense","Expense"),
    ]
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="journal_entries")
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal {self.id} - {self.account.name}"
