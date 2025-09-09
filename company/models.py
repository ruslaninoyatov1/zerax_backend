from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



