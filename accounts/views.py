from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm, UserProfileForm,UserForm
from django.contrib.auth.models import User
from .models import UserProfile
from feedback.models import Feedback, Category
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import logging

# Create your views here.
logger= logging.getLogger('accounts')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            #automatically triggers signal
            logger.info(f"User registered {request.user}")
            messages.success(request,"Account created successfully!, you can now login.")
            # create profile with default role 'employee'
            auth_login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})
    

@login_required
def dashboard_redirect(req):
    
    profile = getattr(req.user, 'userprofile', None)
    role = profile.role if profile else 'employee'

    if req.user.is_superuser:
        return redirect('/admin/')
    elif role== "admin":
        return redirect('admin_dashboard')
    else:
        return redirect("employee_dashboard")
    
@login_required
def employee_dashboard(req):
    total_feedbacks = Feedback.objects.filter(employee=req.user).count()
    active_feedbacks = Feedback.objects.filter(employee=req.user, is_deleted=False).count()
    deleted_feedbacks = Feedback.objects.filter(employee=req.user, is_deleted=True).count()

    context = {
        'total_feedbacks': total_feedbacks,
        'active_feedbacks': active_feedbacks,
        'deleted_feedbacks': deleted_feedbacks
    }
    return render(req, 'accounts/employee_dashboard.html',context)

@login_required
def admin_dashboard(request):

    profile = request.user.userprofile
    if profile.role not in ("admin", "superadmin"):
        return redirect("employee_dashboard")

    # Filters
    selected_user = request.GET.get("employee")
    selected_category = request.GET.get("category")

    employees = User.objects.all()
    categories = Category.objects.all()   # FK MODEL

    all_feedbacks = Feedback.objects.filter(is_deleted=False).select_related("employee", "category")

    if selected_user:
        all_feedbacks = all_feedbacks.filter(employee__username=selected_user)

    if selected_category:
        all_feedbacks = all_feedbacks.filter(category_id=selected_category)

    return render(request, "accounts/admin_dashboard.html", {
        "employees": employees,
        "categories": categories,
        "selected_user": selected_user,
        "selected_category": selected_category,
        "all_feedbacks": all_feedbacks,
    })


@login_required
def view_profile(request):
    profile = request.user.userprofile  
    return render(request, "accounts/view_profile.html", {"profile": profile})


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "accounts/edit_profile.html"

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile = profile_form.save(commit=False)
            profile.modified_by = request.user
            profile.save()

            logger.info(f"Profile updated by {request.user.username}")

            return redirect("view_profile")

        logger.warning(f"Profile update failed for {request.user.username}")

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })
    





