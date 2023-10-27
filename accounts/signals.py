# signals.py

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import LoginLogoutHistory
from django.utils import timezone

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    # Find the latest login record for the user and update the logout time
    latest_login = LoginLogoutHistory.objects.filter(user=user).latest('login_time')
    latest_login.logout_time = timezone.now()
    latest_login.save()
