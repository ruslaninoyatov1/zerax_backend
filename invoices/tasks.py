# invoices/tasks.py
from celery import shared_task

from invoices.models import Invoice


@shared_task
def test_task():
    print("✅ RabbitMQ orqali Celery ishlayapti!")
    return "Celery OK"
@shared_task
def send_due_invoice_reminders():
    invoices = Invoice.objects.filter(is_paid=False)
    for invoice in invoices:
        print(f"🔔 Reminder: Invoice {invoice.id} hali to‘lanmagan!")
    return f"{invoices.count()} ta to‘lanmagan invoice uchun eslatma yuborildi"