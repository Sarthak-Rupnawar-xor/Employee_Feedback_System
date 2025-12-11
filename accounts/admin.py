from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','role','created_at','is_deleted','modified_by','modified_at')
    list_filter = ('role','is_deleted')
    search_fields= ('user__username', 'user__email')

    def save_model(self, req, obj, form, change):
        obj.modified_by = req.user
        super().save_model(req,obj, form, change)

class CustomUserAdmin(UserAdmin):
    actions=['soft_delete_selected']

    def soft_delete_selected(self, request, queryset):
        count= queryset.update(is_active=False)
        self.message_user(request, f"{count} users marked as inactive (soft deleted)")
    
    list_display=['username','email','first_name','last_name','is_staff','is_active']

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)