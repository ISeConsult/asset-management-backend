from django.contrib import admin
from apps.licence.models import (
  LicenseCategoryTypes,
  LicenseCategory,
  License,
  LicenseCheckOut,
  LicenseHistory
)


# Base Admin Class
class BaseAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return tuple(field.name for field in self.model._meta.fields)


# Model Registrations
@admin.register(
LicenseCategoryTypes,
  LicenseCategory,
  License,
  LicenseCheckOut,
  LicenseHistory,
)
class AssetAdmin(BaseAdmin):
    pass
