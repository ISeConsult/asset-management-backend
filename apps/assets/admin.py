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
    AssetModelCategory,
    AssetManufacturer,
    AssetModel,
    AssetLocation,
    AssetsHistory,
    Company,
    ComponentHistory,
    Components,
    ComponentCheckIn,
    ComponentCheckOut,
    ComponentRequest,
    AssetAudit
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
    AssetModelCategory,
    AssetManufacturer,
    AssetModel,
    AssetLocation,
    Company,
    Components,
    ComponentCheckIn,
    ComponentCheckOut,
    ComponentRequest,
    AssetsHistory,
    ComponentHistory,
    AssetAudit,
)
class AssetAdmin(BaseAdmin):
    pass
