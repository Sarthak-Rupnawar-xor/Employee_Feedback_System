import logging
import traceback
from django.utils import timezone

logger = logging.getLogger('django')

class ExceptionLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #print("ExceptionLoggingMiddleware")
        try:
            response = self.get_response(request)
            return response

        except Exception as e:
            user = getattr(request, 'user', None)
            username = user.username if user and user.is_authenticated else 'Anonymous'

            logger.critical(
                f"\n[EXCEPTION] {timezone.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
                f"User: {username}\n"
                f"Path: {request.path}\n"
                f"Error: {e}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            raise
