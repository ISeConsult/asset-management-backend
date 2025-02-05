from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.utils.timezone import now
from .models import UserActivity
from django.contrib.auth import get_user_model
import threading

User = get_user_model()

# Exclude system apps
excluded_apps = [
    "auth",
    "contenttypes",
    "admin",
    "sessions",
    "django_celery_results",
    "django_celery_beat",
    "post_office",
    "userActivities",
    "people",
]

# Get all models except excluded ones
models_to_track = [
    model for model in apps.get_models() if model._meta.app_label not in excluded_apps
]

# Thread-local data to store request info
_request_local = threading.local()


def get_current_request():
    return getattr(_request_local, "request", None)


def set_current_request(request):
    _request_local.request = request


# Create a signal handler dynamically for each model
for model in models_to_track:

    @receiver(post_save, sender=model)
    def log_save_activity(sender, instance, created, **kwargs):
        request = get_current_request()
        user = getattr(request, "user", None) if request else None

        if user:
            action_type = "created" if created else "updated"
            description = f"{sender.__name__} instance {'created' if created else 'updated'} with ID {instance.pk}"

            UserActivity.objects.create(
                user=user,
                action_type=action_type,
                description=description,
                ip_address=(
                    getattr(request, "META", {}).get("REMOTE_ADDR") if request else None
                ),
                user_agent=(
                    getattr(request, "META", {}).get("HTTP_USER_AGENT")
                    if request
                    else None
                ),
                timestamp=now(),
            )

    @receiver(post_delete, sender=model)
    def log_delete_activity(sender, instance, **kwargs):
        request = get_current_request()
        user = getattr(request, "user", None) if request else None

        if user:
            description = f"{sender.__name__} instance deleted with ID {instance.pk}"

            UserActivity.objects.create(
                user=user,
                action_type="deleted",
                description=description,
                ip_address=(
                    getattr(request, "META", {}).get("REMOTE_ADDR") if request else None
                ),
                user_agent=(
                    getattr(request, "META", {}).get("HTTP_USER_AGENT")
                    if request
                    else None
                ),
                timestamp=now(),
            )
