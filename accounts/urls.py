from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('register/',views.register, name='register'),
    path("dashboard_redirect/",views.dashboard_redirect, name='dashboard_redirect'),
    path("dashboard/employee/",views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/admin/',views.admin_dashboard, name='admin_dashboard'),
    path('edit-profile/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/', views.view_profile,name='view_profile' )
]
