from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import arrow

from apps.people.utils import send_login_credentials

# Create your models here.


class Role(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    STAT = (("active", "Active"), ("inActive", "InActive"))
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    department_code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(
        max_length=255,
    )
    manager = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STAT, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.department_code:
            self.department_code = "ISE" + "-" + uuid.uuid4().hex[:6]

        return super().save(*args, **kwargs)


class User(AbstractUser):
    # first_name, last_name, username, email already exist in AbstractUser
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    employee_no = models.CharField(max_length=300, unique=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True
    )
    location = models.CharField(max_length=300, null=True, blank=True)
    login_enabled = models.BooleanField(default=True)
    password_changed = models.BooleanField(default=False)
    password_expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tesr = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username

    def generate_temporal_password(self):
        passw = uuid.uuid4().hex[:8]
        hashed_password = make_password(passw)
        send_login_credentials(self.email, passw)
        return hashed_password

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0].strip()

        if not self.password:
            self.password = self.generate_temporal_password()
            self.password_expiry = arrow.now().shift(minutes=+3).datetime

        super().save(*args, **kwargs)
