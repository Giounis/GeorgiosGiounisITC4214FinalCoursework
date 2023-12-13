#middleware.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
#Middleware for the admin 
class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and hasattr(request, 'user') and request.user.profile.role != 'admin':
            # Redirect or handle unauthorized access as needed
            return HttpResponseForbidden("You are not authorized to access this page.")
        return self.get_response(request)
