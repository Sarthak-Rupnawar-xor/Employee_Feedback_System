from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Feedback(models.Model):

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length= 200)
    message = models.TextField()
    submitted_at= models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.employee.username}"
