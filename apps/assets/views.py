import datetime
import arrow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets,status,permissions
from rest_framework.response import Response
from django.db import transaction
from apps.people.models import User
from apps.people.permissions import TokenRequiredPermission,AdminCheckPermission
from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetAssignment,
    AssetRequest,
    LicenseHistory,
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
from apps.assets.serializers import (
    AssetAssignmentHistorySerializer,
    AssetCategorySerializer,
    AssetAssignmentCreateUpdateSerializer,
    AssetAssignmentListSerializer,
    AssetCreateUpdateSerializer,
    AssetHistoryCreateUpdateSerializer,
    AssetHistoryListSerializer,
    AssetListSerializer,
    AssetRequestCreateUpdateSerializer,
    AssetRequestListSerializer,
    LicenseHistoryListSerializer,
    LicenseCheckoutCreateUpdateSerializer,
    LicenseCheckoutListSerializer,
    MaintenanceRequestCreateUpdateSerializer,
    MaintenanceRequestListSerializer,
    AssetStatusSerializer,
    SoftwareCategorySerializer,
    AssetReturnCreateUpdateSerializer,
    AssetReturnListSerializer,
    AssetSupplierSerializer,
    SoftwareLicencesCreateUpdateSerializer,
    SoftwareLicencesListSerializer,
)
# Create your views here.

class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    

class AssetStatusViewSet(viewsets.ModelViewSet):
    queryset = AssetStatus.objects.all()
    serializer_class = AssetStatusSerializer
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    


class SoftwareCategoryViewSet(viewsets.ModelViewSet):
    queryset = SoftwareCategory.objects.all()
    serializer_class = SoftwareCategorySerializer
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    


class AssetViewset(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    permission_classes = [TokenRequiredPermission, AdminCheckPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCreateUpdateSerializer
        return AssetListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["name", "category", "status","purchase_date","purchase_price","serial_no","image","order_number","condition","model","tag"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        

        if request.FILES.get('image'):
            data['image'] = request.FILES.get('image')


        if not AssetCategory.objects.filter(id=data.get('category')).exists():
            return Response(
                {"success": False, "info": "Asset category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        if not AssetStatus.objects.filter(id=data.get('status')).exists():
            return Response(
                {"success": False, "info": "Asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if data.get('supplier') and not AssetSupplier.objects.filter(id=data.get('supplier')).exists():
            return Response(
                {"success": False, "info": "Asset supplier does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset added successfully"}, status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["get"], permission_classes=[TokenRequiredPermission], url_path='asset-history')
    def asset_history(self, request, *args, **kwargs):
        asset_uid = kwargs.get('asset_uid')
        if not asset_uid:
            return Response({"success": False, "info": "Asset UID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        asset = get_object_or_404(Asset, uid=asset_uid)
        queryset = Asset.objects.filter(asset=asset)
        serializer = AssetHistoryListSerializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )


    @action(detail=False, methods=["get"], permission_classes=[TokenRequiredPermission], url_path='all-asset-histories')
    def all_asset_histories(self, request, *args, **kwargs):
        queryset = Asset.objects.all()
        serializer = AssetHistoryListSerializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    


class AssetRequestViewSet(viewsets.ModelViewSet):
    queryset = AssetRequest.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetRequestCreateUpdateSerializer
        return AssetRequestListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["user", "asset","comment",]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        

        asset = Asset.objects.filter(id=data.get('asset')).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        if not User.objects.filter(id=data.get('user')).exists():
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not asset.requestable or not asset.status.name == "ready-to-deploy":
            return Response(
                {"success": False, "info": "Asset is not requestable at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if asset.requestable and not asset.status.name == "ready-to-deploy":
            return Response(
                {"success": False, "info": "Asset not ready to deploy"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        
        now = datetime.datetime.now().date()
        data["request_date"] = now
        print(now)


        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset request added successfully"}, status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=["post"], permission_classes=[TokenRequiredPermission, AdminCheckPermission], url_path='asset-request-approval')
    def asset_request_approval(self, request, *args, **kwargs):
        asset_request_id = request.data.get('asset_request')
        if not asset_request_id:
            return Response({"success": False, "info": "Asset Request UID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        request_status = request.data.get('status')

        if not request_status:
            return Response({"success": False, "info": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request_status not in ["approved", "rejected"]:
            return Response({"success": False, "info": "Invalid status provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        asset_request = get_object_or_404(AssetRequest, id=asset_request_id)
        
        if request_status == "approved":
            try:
                with transaction.atomic():
                    asset = asset_request.asset
                    asset.status = AssetStatus.objects.get(name="deployed")
                    asset.current_assignee = asset_request.user
                    asset.requestable = False
                    asset.save(update_fields=['status', 'current_assignee', 'requestable'])
                    
                    AssetAssignment.objects.create(
                        asset=asset_request.asset,
                        user=asset_request.user,
                        approved_by = request.user.username,
                    )
                    
                    asset_request.status = 'approved'
                    asset_request.approval_date = datetime.datetime.now().date()
                    asset_request.save(update_fields=['status', 'approval_date'])

                return Response({"success": True, "info": "Asset request approved successfully"}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"success": False, "info": "Failed to approve asset request: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request_status == "rejected":
            asset_request.status = 'rejected'
            asset_request.rejection_date = datetime.datetime.now().date()
            asset_request.save(update_fields=['status', 'rejection_date'])
            return Response({"success": True, "info": "Asset request rejected successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"success": False, "info": "Invalid status provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        



class AssetAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAssignment.objects.all()
    permission_classes = [TokenRequiredPermission, AdminCheckPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetAssignmentCreateUpdateSerializer
        return AssetAssignmentListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["user", "asset"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        asset = Asset.objects.filter(id=data.get('asset')).first()
        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not asset.requestable or not asset.status.name == "ready-to-deploy":
            return Response(
                {"success": False, "info": "Asset is not requestable at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if asset.requestable and not asset.status.name == "ready-to-deploy":
            return Response(
                {"success": False, "info": "Asset not ready to deploy"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        user = User.objects.get(id=data.get('user'))
        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        stat = AssetStatus.objects.get(name="deployed")
        if not stat:
            return Response(
                {"success": False, "info": "Asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        asset.current_assignee = user
        asset.requestable = False
        asset.status = stat
        asset.save(update_fields=['current_assignee', 'requestable', 'status'])
        
        data['approved_by'] = request.user.username
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset assignment added successfully"}, status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["get"], permission_classes=[TokenRequiredPermission], url_path='asset-assignment-history')
    def asset_assignment_history(self, request, *args, **kwargs):
        asset_uid = kwargs.get('asset_uid')
        if not asset_uid:
            return Response({"success": False, "info": "Asset UID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        asset = get_object_or_404(Asset, uid=asset_uid)
        queryset = AssetAssignment.objects.filter(asset=asset)
        serializer = AssetAssignmentHistorySerializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )


    @action(detail=False, methods=["get"], permission_classes=[TokenRequiredPermission], url_path='all-assignment-histories')
    def all_asset_assignment_history(self, request, *args, **kwargs):
        queryset = AssetAssignment.objects.all()
        serializer = AssetAssignmentHistorySerializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )


class AssetReturnViewSet(viewsets.ModelViewSet):
    queryset = AssetReturn.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetReturnCreateUpdateSerializer
        return AssetReturnListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["asset"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            

        asset = Asset.objects.filter(id=data.get('asset')).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user_id = request.user.id
        data['user'] = user_id
        user = User.objects.filter(id=user_id)


        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        asset.current_assignee = None
        asset.requestable = True
        asset.save(update_fields=['current_assignee', 'requestable'])
        


        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset return added successfully"}, status=status.HTTP_201_CREATED
        )
    

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return MaintenanceRequestCreateUpdateSerializer
        return MaintenanceRequestListSerializer
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["asset"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        

        asset = Asset.objects.filter(id=data.get('asset')).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user_id = request.user.id
        data['user'] = user_id

        user = User.objects.get(id=user_id)

        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        # asset.status = AssetStatus.objects.get(name="out-for-repair")
        # asset.save(update_fields=['status'])
        
        data['report_date'] = datetime.datetime.now().date()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Maintenance request added successfully"}, status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=["post"], permission_classes=[TokenRequiredPermission, AdminCheckPermission], url_path='maintenance-update')
    def maintenance_update(self, request, *args, **kwargs):
        maintenance_id = request.data.get('maintenance_id')
        maintenance_status = request.data.get('status')
        if not maintenance_id:
            return Response({"success": False, "info": "Maintenance Request UID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not maintenance_status:
            return Response({"success": False, "info": "Maintenance Status not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        maintenance_request = get_object_or_404(MaintenanceRequest, id=maintenance_id)
        maintenance_request.status = maintenance_status
        maintenance_request.save(update_fields=['status'])

        return Response({"success": True, "info": "Maintenance request updated successfully"}, status=status.HTTP_200_OK)

class AssetSupplierViewSet(viewsets.ModelViewSet):
    queryset = AssetSupplier.objects.all()
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"
    serializer_class = AssetSupplierSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    


class SoftwareLicencesViewSet(viewsets.ModelViewSet):
    queryset = SoftwareLicences.objects.all()
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SoftwareLicencesCreateUpdateSerializer
        return SoftwareLicencesListSerializer
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["name", "product_key", "category", "purchase_date"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Software licence added successfully"}, status=status.HTTP_201_CREATED
        )

    

class LicenceCheckoutViewset(viewsets.ModelViewSet):
    queryset = LicenseCheckout.objects.all()
    permission_classes = [TokenRequiredPermission,AdminCheckPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return LicenseCheckoutCreateUpdateSerializer
        return LicenseCheckoutListSerializer
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def validate_related_fields(self, data):
        related_fields = {
            "user": User,
            "licence": SoftwareLicences,
        }

        for field, model in related_fields.items():
            get_object_or_404(model, uid=data.get(field))

    
    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["user", "licence"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            

        # Validate related fields
        try:
            self.validate_related_fields(data)
        except Exception as e:
            return Response({"success": False, "info": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "License checkout added successfully"}, status=status.HTTP_201_CREATED
        )
    
    @action(detail=False,methods=['get'],permission_classes=[TokenRequiredPermission],url_path='license-checkout-history')
    def license_checkout_history(self,request,pk=None):
        queryset = LicenseHistory.objects.all()
        serializer = LicenseHistoryListSerializer(queryset, many=True)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )