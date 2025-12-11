from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_delete
from .utils import log_activity
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Activity
from django.utils import timezone
import logging

logger= logging.getLogger('accounts')

@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    # automatically log user login time in log activity
    log_activity(user,f"user logged in ")
    logger.info(f"User {user.username} logged in at {timezone.now().strftime('%d-%m-%Y %H:%M:%S')}")

@receiver(user_logged_out)
def log_user_logout(sender, user, request, **kwargs):
    ## automatically log user logout time in log activity
    log_activity(user,f"user logged out ")
    logger.info(f"User {user.username} logged out at {timezone.now().strftime('%d-%m-%Y %H:%M:%S')}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    username= credentials.get('username','Unknown')
    logger.warning(f"Failed login attempts for username: {username}")

@receiver(post_delete, sender= User)
def soft_delete_user_details(sender, instance, **kwargs):
    #soft delete users details after delete user
    Activity.objects.filter(user= instance).update(user=None, action_performed='[Deleted user]')