from django.contrib import admin
from .models import Feedback

# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display= ['employee','subject','message','submitted_at','is_deleted']
    search_fields= ['employee__username','subject','submitted_at','is_deleted']
    
