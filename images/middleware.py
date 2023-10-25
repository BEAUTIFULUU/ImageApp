from django.http import HttpResponseForbidden
from datetime import datetime


class LinkExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expires_str = request.GET.get('expires')
        if expires_str:
            expires = datetime.strptime(expires_str, "%H:%M:%S").time()
            current_time = datetime.now().time()

            if current_time > expires:
                return HttpResponseForbidden("Link has expired")

        response = self.get_response(request)
        return response
