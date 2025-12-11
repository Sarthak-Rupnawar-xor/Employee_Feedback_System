from django.utils import timezone
from .models import Activity
import logging

logger= logging.getLogger(__name__)

class LoginActivityMiddleware:

    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self,request):
        was_logged_in= request.user.is_authenticated
        response= self.get_response(request)
        is_logged_in= request.user.is_authenticated

        if not was_logged_in and is_logged_in:
            Activity.objects.create(
                user=request.user,
                action_performed='User logged in',
            )

            logger.info(f"User '{request.user.username}' logged in at {timezone.now()}")
        
        return response
    
class LogoutActivityMiddleware:

    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self, request):
        was_logged_in= request.user.is_authenticated
        response= self.get_response(request)
        is_logged_in= request.user.is_authenticated

        if was_logged_in and not is_logged_in:
            Activity.objects.create(
                user=None,
                action_performed= "User logged out",
            )

            logger.info(f"User '{request.user.username}' logged out at {timezone.now()}")
        return response