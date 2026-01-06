from feedback.models import Feedback
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from activity_log.models import Activity

class FeedbackSerializer(serializers.ModelSerializer):

    employee= serializers.StringRelatedField(read_only= True)

    class Meta:
        model= Feedback
        fields = ['id', 'employee','category','message', 'submitted_at', 'is_deleted']
        read_only_fields = ['id', 'employee','submitted_at', 'is_deleted']

class ProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = UserProfile
        fields = [
            "username", "email",
            "first_name", "last_name",
            "designation", "employee_id", "contact_no",
        ]

    def update(self, instance, validated_data):
        # update user fields
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()

        # update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class ActivityLogSerializer(serializers.ModelSerializer):
    user= serializers.StringRelatedField()

    class Meta:
        model= Activity
        fields= ['activity_id','user','action_performed','activity_time']
        read_only_fields= fields
