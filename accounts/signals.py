from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.dispatch import receiver
from activity_log.models import Activity

@receiver(post_save, sender= User)
def create_user_profile(sender, instance, created,**kwargs):
    #Automatically creates a new profile whenever a new user is created
    if created:
        UserProfile.objects.create(user= instance)

@receiver(post_save, sender= User)
def save_user_profile(sender, instance, **kwargs):
    #Saves userprofile whenever user is saved
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

# @receiver(post_save, sender=UserProfile)
# def log_profile_update(sender, instance, created, **kwargs):
#     if not created:   #  Avoid "profile created" logs
#         user = instance.user
#         Activity.objects.create(
#             user=user,
#             action_performed=f"Profile updated by {user.username}",
#         )

