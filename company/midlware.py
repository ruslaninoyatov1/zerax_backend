# company/middleware.py
from .models import Company
from threading import local

def get_current_company():
    return getattr(local_data, "company_id", None)

def set_current_company(company_id):
    local_data.company_id = company_id

local_data = local()

class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For testing: set company by domain or header
        company_id = request.headers.get("X-Company-ID")
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
                request.company = company
                set_current_company(company.id)
            except Company.DoesNotExist:
                request.company = None
        else:
            request.company = None

        return self.get_response(request)
