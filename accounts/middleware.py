# middleware.py

# Responsible for tracking user login and logout history in the LoginLogoutHistory model.

from django.utils import timezone
from .models import LoginLogoutHistory

class LoginTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Check if a record already exists for this login session (for example, after a server restart)
            existing_record = LoginLogoutHistory.objects.filter(user=request.user, logout_time__isnull=True).first()

            if existing_record:
                # Update the existing record's login_time
                existing_record.login_time = timezone.now()
                existing_record.save()
            else:
                # Create a new record for login
                LoginLogoutHistory.objects.create(user=request.user, login_time=timezone.now())

        return response
