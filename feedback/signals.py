from django.db.models.signals import post_save, post_delete
from .models import Feedback
from activity_log.utils import log_activity
from django.dispatch import receiver
import logging

logger= logging.getLogger('feedback')

@receiver(post_save, sender=Feedback)
def save_feedback(sender, instance, created,**kwargs):
    user= instance.employee
    if created:
        log_activity(user, f"Feedback submitted (ID {instance.id})")
        logger.info(f"Signal: Feedback created by {user.username} (ID: {instance.id})")
    else:
        log_activity(user,f"Feedback updated (ID {instance.id})")
        logger.info(f"Signal: Feedback updated by {user.username} (ID: {instance.id})")

@receiver(post_delete, sender= Feedback)
def delete_feedback(sender, instance, **kwargs):
    user= instance.employee
    log_activity(user, f"Feedback deleted (ID {instance.id})")