from django import forms 
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model= Feedback
        fields= ['subject','message']

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your feedback here...'
            })
        }
