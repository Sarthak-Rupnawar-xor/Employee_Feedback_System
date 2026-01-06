from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):

    name= models.CharField(max_length=50, unique=True)
    contact_person= models.CharField(max_length=50)
    contact_email= models.EmailField()

    def __str__(self):
        return self.name

class Feedback(models.Model):

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    category= models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    message = models.TextField()
    submitted_at= models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.employee.username} - {self.category.name}"
    
