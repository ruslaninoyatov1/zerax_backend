from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Expense
from core.models import Log

@receiver(post_save, sender=Expense)
def log_expense(sender, instance, created, **kwargs):
    if instance.user.role == "accountant":
        Log.objects.create(
            user=instance.user,
            action="create" if created else "update",
            model_name="Expense",
            object_id=instance.id
        )