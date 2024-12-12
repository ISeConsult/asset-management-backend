from apps.assets.models import AssetAssignment, AssetRequest, MaintenanceRequest,   Asset
from apps.people.models import Department, Role, User
from rest_framework import serializers


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

    def get_total_users(self, obj):
        users = User.objects.filter(department=obj)
        if users:
            return users.count()
        return 0
    
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

    # calculate the total amounts for all the below and return them
    assigned_assets = serializers.SerializerMethodField()
    asset_requests = serializers.SerializerMethodField()
    maintenance_requests = serializers.SerializerMethodField()
    # current_assets = serializers.SerializerMethodField()

    # def get_current_assets(self, obj):
    #     assets = Asset.objects.filter(user=obj)
    #     if assets:
    #         return assets.count()
    #     return 0

    def get_assigned_assets(self, obj):
        # Get all asset assignments for the user
        asi_assets = AssetAssignment.objects.filter(user=obj)
        
        if asi_assets.exists():
            # Initialize a list to store asset details
            assets_details = []
            
            # Loop through each asset assignment and extract the asset details
            for assignment in asi_assets:
                asset = assignment.asset
                assets_details.append({
                    "asset_uid":asset.uid,
                    "asset_name": asset.name,
                    "model": asset.model,
                    "serial_no": asset.serial_no
                })
            
            # Return the total count and the list of asset details
            return {
                "total": asi_assets.count(),
                "assets": assets_details
            }
    
    # Return an empty dictionary if no assets are assigned
        return {}


    
    def get_asset_requests(self, obj):
        asi_requests = AssetRequest.objects.filter(user=obj)
        
        if asi_requests.exists():
            # Initialize a list to store asset details
            assets_details = []
            
            # Loop through each asset assignment and extract the asset details
            for assignment in asi_requests:
                asset = assignment.asset
                assets_details.append({
                    "asset_uid":asset.uid,
                    "asset_name": asset.name,
                    "model": asset.model,
                    "request_date": assignment.request_date
                })
            
            # Return the total count and the list of asset details
            return {
                "total": asi_requests.count(),
                "assets": assets_details
            }
    def get_maintenance_requests(self, obj):
        mtnc_requests = MaintenanceRequest.objects.filter(user=obj)
        if mtnc_requests.exists():
            return mtnc_requests.count()
        
        return 0

    def get_department(self, obj):
        if obj.department:
            return {
                "id": obj.department.id,
                "uid": obj.department.uid,
                "name": obj.department.name,
            }

        return None

    def get_role(self, obj):
        if obj.role:
            return {"id": obj.role.id, "name": obj.role.name}

        return None

    class Meta:
        model = User
        fields = "__all__"



