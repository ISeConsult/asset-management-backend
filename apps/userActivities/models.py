from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class UserActivity(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activities", null=True, blank=True
    )
    action_type = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.timestamp}"
