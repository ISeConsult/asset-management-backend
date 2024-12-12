from django.contrib import admin
from apps.people.models import Department, Role, User

# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Department._meta.fields)
    search_fields = ["name"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Role._meta.fields)
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in User._meta.fields)
    search_fields = ["first_name", "last_name", "username"]
