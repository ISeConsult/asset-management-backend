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
from rest_framework import serializers

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = "__all__"


class AssetAssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAssignment
        fields = "__all__"


class AssetAssignmentListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self,obj):
        if obj.status:
            return{
                'id':obj.status.id,
                'uid':obj.status.uid,
                'name':obj.status.name

            }

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    
    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}
    class Meta:
        model = AssetAssignment
        fields = "__all__"


class AssetHistoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetHistory
        fields = "__all__"

    
class AssetHistoryListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    
    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
        
        return {}

    class Meta:
        model = AssetHistory
        fields = "__all__"



class AssetRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRequest
        fields = "__all__"


class AssetRequestListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    
    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}
    
    class Meta:
        model = AssetRequest
        fields = "__all__"


class MaintenanceRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"


class MaintenanceRequestListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    
    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}

    class Meta:
        model = MaintenanceRequest
        fields = "__all__"


class AssetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetStatus
        fields = "__all__"


class SoftwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareCategory
        fields = "__all__"


class AssetReturnCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetReturn
        fields = "__all__"


class AssetReturnListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    
    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}
    
    class Meta:
        model = AssetReturn
        fields = "__all__"


class AssetSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetSupplier
        fields = "__all__"


class SoftwareLicencesCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareLicences
        fields = "__all__"


class SoftwareLicencesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftwareLicences
        fields = "__all__"



class AssetAssignmentHistorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()
     

    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}
    
    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
    
        return {}
    class Meta:
        model = AssetAssignment
        fields = "__all__"

class LicenseHistoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseHistory
        fields = "__all__"


class LicenseHistoryListSerializer(serializers.ModelSerializer):
    asset = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_asset(self,obj):
        if obj.asset:
            return {
                'id':obj.asset.id,
                'uid':obj.asset.uid,
                'name':obj.asset.name,
            }
        return {}
    

    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}

    class Meta:
        model = LicenseHistory
        fields = "__all__"


class LicenseCheckoutCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseCheckout
        fields = "__all__"


class LicenseCheckoutListSerializer(serializers.ModelSerializer):
    licence = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_licence(self,obj):
        if obj.licence:
            return {
                'id':obj.licence.id,
                'uid':obj.licence.uid,
                'name':obj.licence.username,
            }
    
        return {}
    

    def get_user(self,obj):
        if obj.user:
            return {
                'id':obj.user.id,
                'uid':obj.user.uid,
                'name':obj.user.username,
            }
    
        return {}

    class Meta:
        model = LicenseCheckout
        fields = "__all__"


class AssetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class AssetListSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    current_assignee = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self,obj):
        if obj.category:
            return {
                'id':obj.category.id,
                'uid':obj.category.uid,
                'name':obj.category.name,
            }
    
        return {}

    def get_status(self,obj):
        if obj.status:
            return {
                'id':obj.status.id,
                'uid':obj.status.uid,
                'name':obj.status.name,
            }
    
        return {}

    def get_supplier(self,obj):
        if obj.supplier:
            return {
                'id':obj.supplier.id,
                'uid':obj.supplier.uid,
                'name':obj.supplier.name,
            }

        return {}
    

    def get_current_assignee(self,obj):
        if obj.current_assignee:
            return {
                'id':obj.current_assignee.id,
                'uid':obj.current_assignee.uid,
                'name':obj.current_assignee.username,
            }
    
        return {}
    class Meta:
        model = Asset
        fields = "__all__"