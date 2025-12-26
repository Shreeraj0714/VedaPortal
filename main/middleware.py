from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import messages  # Import messages

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            stored_session_key = cache.get(f'user_session_{request.user.id}')

            if stored_session_key and current_session_key != stored_session_key:
                # Add a message before logging out
                messages.error(request, "You have been logged out because someone else logged into this account.")
                logout(request)
                return redirect('login') 

        response = self.get_response(request)
        return response