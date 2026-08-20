from django.contrib.auth.signals import user_logged_in
from .models import UserActivityLog
from django.utils import timezone

def log_user_activity(sender, user, request, **kwargs):
    UserActivityLog.objects.get_or_create(
        user=user,
        date=timezone.now().date()
    )

user_logged_in.connect(log_user_activity)