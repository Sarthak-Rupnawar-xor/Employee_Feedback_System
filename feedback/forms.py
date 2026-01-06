from django import forms 
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model= Feedback
        fields= ['category','message']

        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your feedback here...'
            })
        }
