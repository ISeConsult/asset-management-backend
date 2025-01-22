from django.contrib import admin
from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetCategoryTypes,
    AssetCheckIn,
    AssetCheckOut,
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
    Components,
    ComponentCheckIn,
)


# Base Admin Class
class BaseAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return tuple(field.name for field in self.model._meta.fields)


# Model Registrations
@admin.register(
    Asset,
    AssetCategoryTypes,
    AssetCategory,
    AssetCheckIn,
    AssetCheckOut,
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
    Components,
    ComponentCheckIn,
)
class AssetAdmin(BaseAdmin):
    pass
