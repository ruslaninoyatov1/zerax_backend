# main/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Redis broker va RabbitMQ backend ishlatish uchun:
app.conf.broker_url = 'amqp://guest:guest@rabbitmq:5672//'
app.conf.result_backend = 'redis://redis:6379/0'

# Django settings.py ichidan CELERY konfiguratsiyasini olish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha app’larning tasks.py fayllarini avtomatik yuklash
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
