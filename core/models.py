from django.db import models
from django.conf import settings
from django.utils import timezone


class Log(models.Model):
    ACTIONS_CHOICES = [
        ('create','Create'),
        ('update','Update'),
        ('delete','Delete')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    action = models.CharField(max_length=10,choices=ACTIONS_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email}  {self.action}  {self.model_name}  {self.object_id}"