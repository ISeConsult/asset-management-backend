from apps.assets.models import (
    AssetCheckIn,
    AssetRequest,
    AssetMaintenanceRequest,
    Asset,
    Components,
)
from apps.assets.serializers import AssetListSerializer, ComponentsListSerializer
from apps.licence.models import License
from apps.licence.serializers import LicenseListSerializer
from apps.people.models import Department, Role, User
from rest_framework import serializers
from decouple import config


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"


class DepartmentCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentListSerializer(serializers.ModelSerializer):
    total_users = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    assets = serializers.SerializerMethodField()
    licenses = serializers.SerializerMethodField()
    consumables = serializers.SerializerMethodField()
    accessories = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_assets(self, obj):
        assets = Asset.objects.filter(current_assignee__department__id=obj.id)
        if assets:
            return assets.count()
        return 0

    def get_licenses(self, obj):
        licenses = License.objects.filter(licensed_to__department__id=obj.id)
        if licenses:
            return licenses.count()
        return 0

    def get_consumables(self, obj):
        consumable = Asset.objects.filter(
            current_assignee__department__id=obj.id,
            category__asset_type__name="consumables",
        )
        if consumable:
            return consumable.count()
        return 0

    def get_accessories(self, obj):
        accessory = Asset.objects.filter(
            current_assignee__department__id=obj.id,
            category__asset_type__name="accessories",
        )
        if accessory:
            return accessory.count()
        return 0

    def get_total_users(self, obj):
        users = User.objects.filter(department=obj)
        if users:
            return users.count()
        return 0

    def get_manager(self, obj):
        if obj.manager:
            return {
                "id": obj.manager.id,
                "uid": obj.manager.uid,
                "full_name": f"{obj.manager.first_name} {obj.manager.last_name}",
                "email": obj.manager.email,
            }

        return None

    def get_image(self, obj):
        if obj.image:
            return config("BASE_URL") + obj.image.url

    def get_company(self, obj):
        if obj.company:
            return {
                "id": obj.company.id,
                "uid": obj.company.uid,
                "name": obj.company.company_name,
            }

        return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "name": obj.location.location_name,
            }

    class Meta:
        model = Department
        fields = "__all__"


class UserCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    assigned_assets = serializers.SerializerMethodField()
    asset_requests = serializers.SerializerMethodField()
    maintenance_requests = serializers.SerializerMethodField()
    assets = serializers.SerializerMethodField()
    asset_list = serializers.SerializerMethodField()
    licenses = serializers.SerializerMethodField()
    license_list = serializers.SerializerMethodField()
    consumables = serializers.SerializerMethodField()
    consumable_list = serializers.SerializerMethodField()
    accessories = serializers.SerializerMethodField()
    accessories_list = serializers.SerializerMethodField()
    components = serializers.SerializerMethodField()
    components_list = serializers.SerializerMethodField()

    def get_image(self, obj):
        return config("BASE_URL") + obj.image.url if obj.image else None

    def get_department(self, obj):
        return {
            "id": obj.department.id,
            "uid": obj.department.uid,
            "name": obj.department.name,
        } if obj.department else None

    def get_role(self, obj):
        return {
            "id": obj.role.id,
            "name": obj.role.name,
        } if obj.role else None

    def get_assets(self, obj):
        return Asset.objects.filter(current_assignee=obj).count()

    def get_asset_list(self, obj):
        assets = Asset.objects.filter(current_assignee=obj)
        return AssetListSerializer(assets, many=True).data if assets.exists() else None

    def get_licenses(self, obj):
        return License.objects.filter(licensed_to=obj).count()

    def get_license_list(self, obj):
        licenses = License.objects.filter(licensed_to=obj)
        return LicenseListSerializer(licenses, many=True).data if licenses.exists() else None

    def get_consumables(self, obj):
        return Asset.objects.filter(current_assignee=obj, category__name="consumables").count()

    def get_consumable_list(self, obj):
        consumables = Asset.objects.filter(current_assignee=obj, category__name="consumables")
        return AssetListSerializer(consumables, many=True).data if consumables.exists() else None

    def get_accessories(self, obj):
        return Asset.objects.filter(current_assignee=obj, category__name="accessories").count()

    def get_accessories_list(self, obj):
        accessories = Asset.objects.filter(current_assignee=obj, category__name="accessories")
        return AssetListSerializer(accessories, many=True).data if accessories.exists() else None

    def get_components(self, obj):
        return Components.objects.filter(current_assignee=obj).count()

    def get_components_list(self, obj):
        components = Components.objects.filter(current_assignee=obj)
        return ComponentsListSerializer(components, many=True).data if components.exists() else None

    def get_assigned_assets(self, obj):
        assigned_assets = AssetCheckIn.objects.filter(user=obj)
        if assigned_assets.exists():
            return {
                "total": assigned_assets.count(),
                "assets": [
                    {
                        "asset_uid": asset.asset.uid,
                        "asset_name": asset.asset.name,
                        "model": asset.asset.asset_model.name,
                        "serial_no": asset.asset.serial_no,
                    }
                    for asset in assigned_assets
                ],
            }
        return {}

    def get_asset_requests(self, obj):
        asset_requests = AssetRequest.objects.filter(user=obj)
        if asset_requests.exists():
            return {
                "total": asset_requests.count(),
                "assets": [
                    {
                        "asset_uid": asset.asset.uid,
                        "asset_name": asset.asset.name,
                        "model": asset.asset.asset_model.name,
                        "request_date": asset.request_date,
                    }
                    for asset in asset_requests
                ],
            }
        return {}

    def get_maintenance_requests(self, obj):
        return AssetMaintenanceRequest.objects.filter(user=obj).count()

    class Meta:
        model = User
        fields = "__all__"
