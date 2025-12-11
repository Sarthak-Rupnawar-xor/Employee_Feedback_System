from django.http import HttpResponseNotFound

class Force404Middleware:
    
    #This forces Django to return a simple 404 page even when DEBUG=True

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return HttpResponseNotFound("Page Not Found (404)")

        return response
