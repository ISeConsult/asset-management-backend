from django.contrib import admin
from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetAssignment,
    AssetRequest,
    MaintenanceRequest,
    AssetHistory,
    AssetReturn,
    AssetSupplier,
    AssetStatus,
    SoftwareCategory,
    SoftwareLicences,
    LicenseHistory,
    LicenseCheckout
)
# Register your models here.


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in Asset._meta.fields)
    search_fields = ["name", "category__name"]

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetCategory._meta.fields)
    search_fields = ["name", "description"]

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetAssignment._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(AssetRequest)
class AssetRequestAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetRequest._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in MaintenanceRequest._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(AssetHistory)
class AssetHistoryAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetHistory._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(AssetReturn)
class AssetReturnAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetReturn._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(AssetSupplier)
class AssetSupplierAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetSupplier._meta.fields)
    search_fields = ["name"]


@admin.register(AssetStatus)
class AssetStatusAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in AssetStatus._meta.fields)
    search_fields = ["name"]


@admin.register(SoftwareCategory)
class SoftwareCategoryAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in SoftwareCategory._meta.fields)
    search_fields = ["name"]


@admin.register(SoftwareLicences)
class SoftwareLicencesAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in SoftwareLicences._meta.fields)
    search_fields = ["name"]


@admin.register(LicenseHistory)
class LicenseHistoryAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in LicenseHistory._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]


@admin.register(LicenseCheckout)
class LicenseCheckoutAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in LicenseCheckout._meta.fields)
    search_fields = ["asset__name", "user__first_name", "user__last_name"]




