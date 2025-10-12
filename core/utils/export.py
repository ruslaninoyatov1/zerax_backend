import os
import pandas as pd
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils import timezone
from pathlib import Path

from invoices.models import Invoice
from expenses.models import Expense
from accounting.models import JournalEntry


def generate_report_file(report, export_type="excel"):
    """
    Universal report generator for Invoices, Expenses, or Accounting.
    """
    try:
        reports_dir = Path(settings.MEDIA_ROOT) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        ext = "xlsx" if export_type == "excel" else "pdf"
        filename = f"report_{report.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        filepath = reports_dir / filename

        source = getattr(report, "source", None)
        filters = report.filters or {}

        print(f"DEBUG — Report Source: {source}")
        print(f"DEBUG — Filters: {filters}")

        # --- Ma'lumotlarni olish ---
        if source == "invoices":
            queryset = Invoice.objects.filter(**filters)
            data = list(queryset.values("id", "client_name", "amount", "status", "due_date", "created_at"))
        elif source == "expenses":
            queryset = Expense.objects.filter(**filters)
            data = list(queryset.values("id", "category", "amount", "date", "note", "created_at"))
        elif source == "accounting":
            queryset = JournalEntry.objects.select_related("account").all()
            data = list(queryset.values("id", "account__name", "debit", "credit", "date", "description"))
        else:
            data = [{"error": "Unknown report source"}]

        print(f"DEBUG — Data length: {len(data)}")
        if data:
            print(f"DEBUG — Sample: {data[:1]}")

        # --- Timezone'larni olib tashlash ---
        for row in data:
            for key, value in row.items():
                if hasattr(value, "tzinfo"):
                    # UTC → naive datetime
                    row[key] = value.replace(tzinfo=None)

        # --- Export qilish ---
        if export_type == "excel":
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, engine="openpyxl")

        elif export_type == "pdf":
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.setTitle(f"Report - {report.name}")

            c.drawString(100, 800, f"Report Name: {report.name}")
            c.drawString(100, 780, f"Source: {source}")
            c.drawString(100, 760, f"Export Type: {export_type}")
            c.drawString(100, 740, f"Created: {report.created_at.strftime('%Y-%m-%d %H:%M')}")

            y = 700
            for row in data[:25]:
                line = ", ".join([f"{k}: {v}" for k, v in row.items()])
                c.drawString(80, y, line[:100])
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 800

            c.save()
            with open(filepath, "wb") as f:
                f.write(buffer.getvalue())

        # --- Relative path ---
        relative_path = filepath.relative_to(settings.MEDIA_ROOT)
        report.file.name = str(relative_path).replace("\\", "/")
        report.save(update_fields=["file"])

        return str(filepath)

    except Exception as e:
        print(f"Error generating report: {e}")
        return None
