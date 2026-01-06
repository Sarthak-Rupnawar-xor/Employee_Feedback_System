from django.contrib import admin
from .models import Feedback, Category

# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display= ['employee','category','message','submitted_at','is_deleted']
    search_fields= ['employee__username','category','submitted_at','is_deleted']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','contact_person','contact_email']
    search_fields=['name']
