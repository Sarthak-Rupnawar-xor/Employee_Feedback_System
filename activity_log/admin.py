from django.contrib import admin
from .models import Activity
# Register your models here.

@admin.register(Activity)
class AdminActivity(admin.ModelAdmin):
    list_display= ['activity_id','user','action_performed','activity_time']
    search_fields = ['user__username','action_performed']
    list_filter= ['activity_time']