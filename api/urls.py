from django.urls import path,include
from .views import FeedbackDetailAPIView,FeedbackListAPIView, ProfileAPIView

urlpatterns = [
    path('feedbacks/',FeedbackListAPIView.as_view(), name='api_feedback_list'),
    path('feedbacks/<int:pk>/',FeedbackDetailAPIView.as_view(), name='api_feedback_detail'),
    path('profile/', ProfileAPIView.as_view(), name='profile_view'),
]