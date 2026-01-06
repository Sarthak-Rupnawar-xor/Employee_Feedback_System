import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_Feedback_System.settings')

app = Celery('Employee_Feedback_Syste')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
