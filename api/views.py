from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions, IsAdminUser
from .serializers import FeedbackSerializer, ProfileSerializer,ActivityLogSerializer
from feedback.models import Feedback
from activity_log.models import Activity
from .permissions import IsOwnerOrAdmin
# Create your views here.

#Feedback List api
class FeedbackListAPIView(generics.ListCreateAPIView):

    serializer_class= FeedbackSerializer
    permission_classes= [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        
        user = self.request.user
        role = getattr(user.userprofile, "role", "").lower().strip()

    # Admin & Superadmin view all feedbacks
        if role in ("admin", "superadmin"):
            return Feedback.objects.filter(is_deleted=False).select_related("employee").order_by("-submitted_at")

    # Employee view Only own feedbacks
        return Feedback.objects.filter(is_deleted=False,employee=user).order_by("-submitted_at")       

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

# individual feedback view/edit/delete API
class FeedbackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class= FeedbackSerializer
    permission_classes= [IsAuthenticated,IsOwnerOrAdmin]

    def get_queryset(self):
        user= self.request.user
        role = getattr(user.userprofile, "role", "").lower().strip()

        if role in ("admin", "superadmin"):
            return Feedback.objects.filter(is_deleted=False).select_related("employee").order_by("-submitted_at")
        
        return Feedback.objects.filter(is_deleted=False,employee=user).order_by("-submitted_at")  


#Profile view & update API
class ProfileAPIView(generics.RetrieveUpdateAPIView):

    serializer_class= ProfileSerializer
    permission_classes= [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile
    
#Activity Log API 
class ActivityLogAPIView(viewsets.ModelViewSet):

    queryset= Activity.objects.all().order_by('-activity_time')
    serializer_class=ActivityLogSerializer
    permission_classes= [IsAuthenticated,IsAdminUser]
    http_method_names=['get','delete','head','options']