from celery import shared_task
from core.utils.export import generate_report_file
from reports.models import Report

@shared_task
def generate_report_async(report_id, export_type):
    try:
        report = Report.objects.get(id=report_id)
        file_path = generate_report_file(report, export_type)
        print(f"[CELERY] Report generated: {file_path}")
        return {"status": "success", "file": file_path}
    except Exception as e:
        print(f"[CELERY ERROR] {e}")
        return {"status": "error", "message": str(e)}
