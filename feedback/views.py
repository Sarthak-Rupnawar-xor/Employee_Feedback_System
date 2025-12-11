from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden,Http404
from .exceptions import InvalidFeedbackException
import logging

logger= logging.getLogger('feedback')

# Create your views here.
@login_required
def feedback_list(req):
    feedbacks = Feedback.objects.filter(employee=req.user, is_deleted=False).order_by('-submitted_at')
    return render(req, 'feedback/feedback_list.html', {'feedbacks':feedbacks})

@login_required
def add_feedback(req):
    try:
        if req.method== "POST":
            form= FeedbackForm(req.POST)
            if form.is_valid():
                feedback= form.save(commit=False)
                feedback.employee = req.user
                
                try:
                    feedback.save()
                    messages.success(req,"Feedback added successfully...")
                    logger.info(f"feedback submitted by {req.user.username}")
                    return redirect('feedback_list')
                except Exception as e:
                    logger.critical(f"error saving feedback by {req.user.username}: {e}")
                    messages.error(req,"an error occured while saving feedback, please try again later.")
            else:
                logger.warning(f"Invalid feedback form by {req.user.username}")
        else:
            form= FeedbackForm()

    except InvalidFeedbackException as e:
        logger.critical(f"Unexpected error in add_feedback() {e}")
        messages.error(req, "Something went wrong. Please contact the admin.")
    
    finally:
        logger.info(f"add_feedback executed for {req.user.username}")

    return render(req, 'feedback/feedback_form.html', {'form':form})

@login_required
def delete_feedback(req, feedback_id):

    profile= req.user.userprofile
    if profile.role not in ('admin', 'superadmin'):
        return HttpResponseForbidden("You are not allowed to delete a feedback")
    
    feedback= Feedback.objects.get(id=feedback_id, is_deleted= False)
    feedback.is_deleted= True
    feedback.save()
    messages.success(req,"Feedback deleted successfully...")
    #log_activity(req.user, 'Feedback Deleted by admin')

    return redirect('admin_dashboard')

@login_required
def delete_own_feedback(req, feedback_id):
    try:
        feedback= Feedback.objects.get(id=feedback_id, employee= req.user, is_deleted= False)
    except:
        raise Http404("Feedback not found or already deleted")
    
    if req.method=='POST':
        feedback.is_deleted= True
        feedback.save()
        messages.success(req, "Feedback deleted successfully")
        #log_activity(req.user, 'deleted own feedback')
        return redirect("feedback_list")
    return HttpResponseForbidden("Invalid request")

@login_required
def edit_feedback(request, id):
    try:
        feedback = get_object_or_404(Feedback, pk=id, employee=request.user, is_deleted=False)

        if request.method == 'POST':
            form = FeedbackForm(request.POST, instance=feedback)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Feedback updated successfully!")
                    logger.info(f"Feedback (ID: {id}) updated by {request.user.username}")
                    return redirect('feedback_list')
                except Exception as e:
                    logger.error("Database error while updating the feedback: {e}")
                    messages.error(request,"Something went wrong while updating the feedback, please try again later.")

        else:
            form = FeedbackForm(instance=feedback)
        
    except Feedback.DoesNotExist:
        logger.warning(f"Feedback {id} not not found for user:{request.user.username}")
        messages.error(request,"Feedback does not exist")
        return redirect("feedback_list")
    
    except Exception as e:
        logger.critical("Unexpected error while editing feedback {e}")
        messages.error("an unexpected error occured while editing feedback {id}")

    return render(request, 'feedback/edit_feedback.html', {'form': form})

def test_error(request):
    raise ValueError("Intentional test error")
