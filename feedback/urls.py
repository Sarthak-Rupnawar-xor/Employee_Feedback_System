from django.urls import path
from .views import feedback_list,add_feedback,delete_feedback,delete_own_feedback,edit_feedback,test_error

urlpatterns = [
    path("add/", add_feedback, name='add_feedback'),
    path("list/", feedback_list, name='feedback_list'),
    path('delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('delete-own/<int:feedback_id>/', delete_own_feedback, name='delete_own_feedback'),
    path("edit-own/<int:id>/", edit_feedback, name='edit_feedback'),
    path('test-error/', test_error, name='test_error'),
]