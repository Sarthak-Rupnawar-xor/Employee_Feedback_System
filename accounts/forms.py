from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap class + placeholder for password fields manually
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['designation', 'employee_id', 'contact_no']

        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employee ID'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit contact number'}),
        }

    def clean_contact_no(self):
        contact = self.cleaned_data.get('contact_no')

        if contact and not re.fullmatch(r'[0-9]{10}', contact):
            raise forms.ValidationError("Contact number must be exactly 10 digits.")

        return contact

    def clean_employee_id(self):
        empid = self.cleaned_data.get('employee_id')

        if empid:
            qs = UserProfile.objects.filter(employee_id=empid)

            # Exclude current user's profile if editing
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Employee ID already exists.")

        return empid

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
        }
