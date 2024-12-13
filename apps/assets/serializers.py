from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetLocation,
    AssetManufacturer,
    AssetModel,
    AssetModelCategory,
    AssetCheckIn,
    AssetRequest,
    AssetMaintenanceRequest,
    AssetReturn,
    AssetSupplier,
    AssetStatus,
    Company,
)
from rest_framework import serializers
from decouple import config


class AssetModelCatecorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModelCategory
        fields = "__all__"


class AssetManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetManufacturer
        fields = "__all__"


class AssetModelCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModel
        fields = "__all__"


class AssetModelListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_category(self, obj):
        return (
            {"id": obj.category.id, "uid": obj.category.uid, "name": obj.category.name}
            if obj.category
            else None
        )

    def get_manufacturer(self, obj):
        if obj.manufacturer:
            return AssetManufacturerSerializer(obj.manufacturer).data
        return None

    def get_image(self, obj):
        if obj.image:
            return {"url": config("BASE_URL") + obj.image.url}
        return None

    class Meta:
        model = AssetModel
        fields = "__all__"


class AssetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetStatus
        fields = "__all__"


class AssetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetLocation
        fields = "__all__"


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = "__all__"


class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    def get_image(self, obj):
        if obj.image:
            return {"url": config("BASE_URL") + obj.image.url}
        return None

    class Meta:
        model = Company
        fields = "__all__"


class AssetSupplierCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetSupplier
        fields = "__all__"


class AssetSupplierListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return {"url": config("BASE_URL") + obj.image.url}
        return None

    class Meta:
        model = AssetSupplier
        fields = "__all__"


class AssetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class AssetListSerializer(serializers.ModelSerializer):
    asset_model = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    current_assignee = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_asset_model(self, obj):
        if obj.asset_model:
            return AssetModelListSerializer(obj.asset_model).data
        else:
            return None

    def get_status(self, obj):
        if obj.status:
            return {"id": obj.status.id, "uid": obj.status.uid, "name": obj.status.name}

        else:
            return None

    def get_current_assignee(self, obj):
        if obj.current_assignee:
            return {
                "id": obj.current_assignee.id,
                "uid": obj.current_assignee.uid,
                "full_name": f"{obj.current_assignee.first_name} {obj.current_assignee.last_name}",
            }

        else:
            return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    def get_supplier(self, obj):
        if obj.supplier:
            return AssetSupplierListSerializer(obj.supplier).data

        else:
            return None

    def get_image(self, obj):
        if obj.image:
            return {"url": config("BASE_URL") + obj.image.url}
        return None

    def get_category(self, obj):
        return (
            {"id": obj.category.id, "uid": obj.category.uid, "name": obj.category.name}
            if obj.category
            else None
        )

    class Meta:
        model = Asset
        fields = "__all__"


class AssetRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRequest
        fields = "__all__"


class AssetRequestListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "uid": obj.user.uid,
                "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            }
        else:
            return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    class Meta:
        model = AssetRequest
        fields = "__all__"


class AssetCheckInCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCheckIn
        fields = "__all__"


class AssetCheckInListSerializer(serializers.ModelSerializer):
    asset_request = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_asset_request(self, obj):
        if obj.asset_request:
            return AssetRequestListSerializer(obj.asset_request).data
        else:
            return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    def get_status(self, obj):
        if obj.status:
            return {"id": obj.status.id, "uid": obj.status.uid, "name": obj.status.name}

        else:
            return None

    class Meta:
        model = AssetCheckIn
        fields = "__all__"


class AssetReturnCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetReturn
        fields = "__all__"


class AssetReturnListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.ModelSerializer()
    status = serializers.ModelSerializer()
    location = serializers.ModelSerializer()

    def get_asset(self, obj):
        if obj.asset:
            return AssetListSerializer(obj.asset).data

        return None

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "uid": obj.user.uid,
                "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            }
        else:
            return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    def get_status(self, obj):
        if obj.status:
            return {"id": obj.status.id, "uid": obj.status.uid, "name": obj.status.name}

        else:
            return None

    class Meta:
        model = AssetReturn
        fields = "__all__"


class AssetMaintenanceRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaintenanceRequest
        fields = "__all__"


class AssetMaintenanceRequestListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_asset(self, obj):
        if obj.asset:
            return AssetListSerializer(obj.asset).data

        return None

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "uid": obj.user.uid,
                "full_name": f"{obj.user.first_name} {obj.user.last_name}",
            }
        else:
            return None

    def get_location(self, obj):
        if obj.location:
            return {
                "id": obj.location.id,
                "uid": obj.location.uid,
                "location": obj.location.name,
            }

        else:
            return None

    class Meta:
        model = AssetMaintenanceRequest
        fields = "__all__"
