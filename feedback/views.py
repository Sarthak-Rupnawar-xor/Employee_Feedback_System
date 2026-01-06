from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden,Http404
from .exceptions import InvalidFeedbackException
from django.core.mail import send_mail
from django.conf import settings
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

                    try:
                        category= feedback.category
                        if category and category.contact_email:
                            send_mail(
                                subject= f"New Feedback in {category.name}",
                                message=(
                                    f"Hello {category.contact_person},\n\n"
                                    f"New Feedback has been submitted.\n\n"
                                    f"Employee: {req.user.username}\n"
                                    f"Category: {category.name}\n"
                                    f"Message:\n{feedback.message}\n\n"
                                    f"Thank you."
                                ),
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[category.contact_email],
                                fail_silently=False,
                            )
                    except Exception as e:
                        logger.error("Email sending failed")

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
def edit_feedback(req, id):
    feedback = get_object_or_404(Feedback, pk=id)

    # Only owner can edit
    if feedback.employee != req.user:
        messages.error(req, "You are not allowed to edit this feedback.")
        return redirect("feedback_list")

    old_category = feedback.category  # Track old category

    if req.method == 'POST':
        form = FeedbackForm(req.POST, instance=feedback)

        if form.is_valid():
            updated_feedback = form.save(commit=False)
            updated_feedback.save()

            new_category = updated_feedback.category

            # CASE 1: Category did NOT change → send REPLY/UPDATE email
            if old_category == new_category:
                try:
                    send_mail(
                        subject=f"Feedback Update - {new_category.name}",
                        message=(
                            f"Hello {new_category.contact_person},\n\n"
                            f"The employee '{req.user.username}' updated a previous feedback.\n\n"
                            f"Updated Message:\n\n{updated_feedback.message}\n\n"
                            f"Category: {new_category.name}\n"
                            f"Thank you."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[new_category.contact_email],
                        fail_silently=False,
                    )

                    logger.info(f"Update reply email sent for feedback ID {updated_feedback.id}")

                except Exception as e:
                    logger.error(f"Error sending reply email: {e}")


            # CASE 2: Category CHANGED → send NEW FEEDBACK email
            else:
                try:
                    send_mail(
                        subject=f"New Feedback Submitted - {new_category.name}",
                        message=(
                            f"Hello {new_category.contact_person},\n\n"
                            f"A new feedback was submitted.\n\n"
                            f"Employee: {req.user.username}\n"
                            f"Category: {new_category.name}\n"
                            f"Message:\n{updated_feedback.message}\n\n"
                            f"Thank you."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[new_category.contact_email],
                        fail_silently=False,
                    )

                    logger.info(f"New feedback email sent after category change for feedback ID {updated_feedback.id}")

                except Exception as e:
                    logger.error(f"Error sending new feedback email: {e}")

            messages.success(req, "Feedback updated successfully.")
            return redirect('feedback_list')

    else:
        form = FeedbackForm(instance=feedback)

    return render(req, 'feedback/edit_feedback.html', {'form': form})


def test_error(request):
    raise ValueError("Intentional test error")
