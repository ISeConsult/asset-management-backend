from django.contrib import admin
from apps.userActivities.models import UserActivity

# Register your models here.


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in UserActivity._meta.fields)
