from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import re

class CustomUserCreationForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields= ['designation','employee_id','contact_no']

    def clean_contact_no(self):
        contact = self.cleaned_data['contact_no']

        if contact and not re.fullmatch(r'[0-9]{10}', contact):
            raise forms.ValidationError("Contact number must be exactly 10 digits.")

        return contact

    # ✅ VALIDATION 2 — Duplicate Employee ID
    def clean_employee_id(self):
        empid = self.cleaned_data['employee_id']

        if empid:
            qs = UserProfile.objects.filter(employee_id=empid)

            # Exclude current user
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Employee ID already exists.")

        return empid

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['first_name','last_name']