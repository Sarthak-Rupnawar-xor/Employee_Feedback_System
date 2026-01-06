from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def test_email_task():
    send_mail(
        "Celery Test",
        "Celery + Redis via Ubuntu VM is working!",
        settings.EMAIL_HOST_USER,
        ["sarthakrupnawar46@gmail.com"],
        fail_silently=False,
    )
