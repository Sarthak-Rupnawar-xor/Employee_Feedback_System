from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Activity(models.Model):
    activity_id= models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_performed = models.CharField(max_length=100)
    activity_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['-activity_time']
