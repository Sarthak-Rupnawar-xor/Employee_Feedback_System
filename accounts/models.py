from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ("employee", "Employee"),
        ('admin', "Admin"),
        ('superadmin', 'Super Admin'),
    )

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True,null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    role= models.CharField(max_length=40, choices= ROLE_CHOICES, default='employee')
    is_deleted= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_profiles')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    