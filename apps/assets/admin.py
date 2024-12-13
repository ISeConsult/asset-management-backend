from django.contrib import admin
from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetCheckIn,
    AssetMaintenanceRequest,
    AssetRequest,
    AssetReturn,
    AssetSupplier,
    AssetStatus,
    AssetModelCategory,
    AssetManufacturer,
    AssetModel,
    AssetLocation,
    Company,
)


# Base Admin Class
class BaseAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return tuple(field.name for field in self.model._meta.fields)


# Model Registrations
@admin.register(
    Asset,
    AssetCategory,
    AssetCheckIn,
    AssetMaintenanceRequest,
    AssetRequest,
    AssetReturn,
    AssetSupplier,
    AssetStatus,
    AssetModelCategory,
    AssetManufacturer,
    AssetModel,
    AssetLocation,
    Company,
)
class AssetAdmin(BaseAdmin):
    pass
