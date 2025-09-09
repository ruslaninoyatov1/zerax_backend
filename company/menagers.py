# company/managers.py
from django.db import models
from .midlware import get_current_company

class CompanyQuerySet(models.QuerySet):
    def for_current_company(self):
        company_id = get_current_company()
        if company_id:
            return self.filter(company_id=company_id)
        return self.none()

class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().for_current_company()
