import datetime
import logging
import arrow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction
from apps.assets.pagination import FetchDataPagination
from apps.people.models import User
from apps.people.permissions import TokenRequiredPermission, AdminCheckPermission
from apps.assets.models import (
    Asset,
    AssetCategoryTypes,
    AssetModelCategory,
    AssetManufacturer,
    AssetCategory,
    AssetMaintenanceRequest,
    AssetRequest,
    AssetReturn,
    AssetSupplier,
    AssetStatus,
    AssetModel,
    AssetStatus,
    AssetLocation,
    Company,
    AssetCheckIn,
)
from apps.assets.serializers import (
    AssetCategoryCreateUpdateSerializer,
    AssetCategoryTypesListSerializer,
    AssetCategoryTypesSerializer,
    AssetMaintenanceRequestCreateUpdateSerializer,
    AssetMaintenanceRequestListSerializer,
    AssetSupplierCreateUpdateSerializer,
    AssetSupplierListSerializer,
    AssetModelCatecorySerializer,
    AssetManufacturerSerializer,
    AssetModelCreateUpdateSerializer,
    AssetModelListSerializer,
    AssetLocationSerializer,
    CompanyCreateUpdateSerializer,
    AssetCheckInCreateUpdateSerializer,
    AssetCheckInListSerializer,
    AssetCreateUpdateSerializer,
    AssetListSerializer,
    AssetRequestCreateUpdateSerializer,
    AssetRequestListSerializer,
    AssetStatusSerializer,
    AssetReturnCreateUpdateSerializer,
    AssetReturnListSerializer,
    CompanyListSerializer,
)

logger = logging.getLogger(__name__)

# Create your views here.


class AssetCategoryTypesViewset(viewsets.ModelViewSet):
    queryset = AssetCategoryTypes.objects.all()
    permission_classes = [TokenRequiredPermission]
    pagination_class = FetchDataPagination
    lookup_field = "uid"
    serializer_class = AssetCategoryTypesSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        name = data.get("name")

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCategoryCreateUpdateSerializer
        return AssetCategoryTypesListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        asset_type = data.get("asset_type")
        name = data.get("name")

        if not asset_type:
            return Response(
                {"success": False, "info": "asset_type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ass_type = AssetCategoryTypes.objects.filter(id=asset_type).first()

        if not ass_type:
            return Response(
                {"success": False, "info": "asset_type does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetManufacturerViewset(viewsets.ModelViewSet):
    queryset = AssetManufacturer.objects.all()
    permission_classes = [TokenRequiredPermission]
    serializer_class = AssetManufacturerSerializer
    pagination_class = FetchDataPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not phone:
            return Response(
                {"success": False, "info": "phone is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetLocationViewset(viewsets.ModelViewSet):
    queryset = AssetLocation.objects.all()
    permission_classes = [TokenRequiredPermission]
    serializer_class = AssetLocationSerializer
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        location_name = data.get("location_name")
        address = data.get("address")
        city = data.get("city")
        country = data.get("country")

        if not location_name:
            return Response(
                {"success": False, "info": "location_name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not address:
            return Response(
                {"success": False, "info": "address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not city:
            return Response(
                {"success": False, "info": "city is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not country:
            return Response(
                {"success": False, "info": "country is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CompanyCreateUpdateSerializer
        return CompanyListSerializer

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
        company_name = data.get("company_name")
        location = data.get("location")
        company_mail = data.get("company_mail")
        company_phone = data.get("company_phone")

        if not company_name:
            return Response(
                {
                    "success": False,
                    "info": "company_name is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not location:
            return Response(
                {
                    "success": False,
                    "info": "location is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not company_mail:
            return Response(
                {
                    "success": False,
                    "info": "company_mail is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not company_phone:
            return Response(
                {
                    "success": False,
                    "info": "company_phone is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        loc = AssetLocation.objects.filter(id=location).first()
        if not loc:
            return Response(
                {
                    "success": False,
                    "info": "location does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetModelViewset(viewsets.ModelViewSet):
    queryset = AssetModel.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetModelCreateUpdateSerializer
        return AssetModelListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        name = data.get("name")
        category = data.get("category")
        manufacturer = data.get("manufacturer")

        if not name:
            return Response(
                {
                    "success": False,
                    "info": "name is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not category:
            return Response(
                {
                    "success": False,
                    "info": "category is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not manufacturer:
            return Response(
                {
                    "success": False,
                    "info": "manufacturer is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        cat = AssetModelCategory.objects.filter(id=category).first()
        if not cat:
            return Response(
                {
                    "success": False,
                    "info": "category does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        man = AssetManufacturer.objects.filter(id=manufacturer).first()
        if not man:
            return Response(
                {
                    "success": False,
                    "info": "manufacturer does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetModelCategoryViewset(viewsets.ModelViewSet):
    queryset = AssetModelCategory.objects.all()
    serializer_class = AssetModelCatecorySerializer
    permission_classes = [TokenRequiredPermission]
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

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name")

        if not name:
            return Response(
                {
                    "success": False,
                    "info": "name is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetStatusViewSet(viewsets.ModelViewSet):
    queryset = AssetStatus.objects.all()
    serializer_class = AssetStatusSerializer
    permission_classes = [TokenRequiredPermission, AdminCheckPermission]
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

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name")

        if not name:
            return Response(
                {
                    "success": False,
                    "info": "name is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetViewset(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    permission_classes = [TokenRequiredPermission, AdminCheckPermission]
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCreateUpdateSerializer
        return AssetListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        asset_tag = data.get("asset_tag")
        serial_no = data.get("serial_no")
        asset_model = data.get("asset_model")
        asset_status = data.get("status")
        location = data.get("location")
        category = data.get("category")
        purchase_cost = data.get("purchase_cost")
        supplier = data.get("supplier")
        purchase_date = data.get("purchase_date")

        if not asset_tag:
            return Response(
                {"success": False, "info": "asset_tag is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not serial_no:
            return Response(
                {"success": False, "info": "serial_no is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not asset_model:
            return Response(
                {"success": False, "info": "asset_model is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not asset_status:
            return Response(
                {"success": False, "info": "asset_status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not location:
            return Response(
                {"success": False, "info": "location is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not purchase_cost:
            return Response(
                {"success": False, "info": "purchase_cost is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not category:
            return Response(
                {"success": False, "info": "category is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not supplier:
            return Response(
                {"success": False, "info": "supplier is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not purchase_date:
            return Response(
                {"success": False, "info": "purchase_date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ass_model = AssetModel.objects.filter(id=asset_model)

        if not ass_model.exists():
            return Response(
                {"success": False, "info": "asset model does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ass_status = AssetStatus.objects.filter(id=asset_status)

        if not ass_status.exists():
            return Response(
                {"success": False, "info": "asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        loc = AssetLocation.objects.filter(id=location)
        if not loc.exists():
            return Response(
                {"success": False, "info": "asset location does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cat = AssetCategory.objects.filter(id=category)

        if not cat.exists():
            return Response(
                {"success": False, "info": "asset category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sup = AssetSupplier.objects.filter(id=supplier)

        if not sup.exists():
            return Response(
                {"success": False, "info": "asset supplier does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset added successfully"},
            status=status.HTTP_201_CREATED,
        )

    # @action(
    #     detail=True,
    #     methods=["get"],
    #     permission_classes=[TokenRequiredPermission],
    #     url_path="asset-history",
    # )
    # def asset_history(self, request, *args, **kwargs):
    #     asset_uid = kwargs.get("asset_uid")
    #     if not asset_uid:
    #         return Response(
    #             {"success": False, "info": "Asset UID not provided"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     asset = get_object_or_404(Asset, uid=asset_uid)
    #     queryset = Asset.objects.filter(asset=asset)
    #     serializer = AssetHistoryListSerializer(queryset, many=True)
    #     return Response(
    #         {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     methods=["get"],
    #     permission_classes=[TokenRequiredPermission],
    #     url_path="all-asset-histories",
    # )
    # def all_asset_histories(self, request, *args, **kwargs):
    #     queryset = Asset.objects.all()
    #     serializer = AssetHistoryListSerializer(queryset, many=True)
    #     return Response(
    #         {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
    #     )


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
        required_fields = [
            "user",
            "asset",
            "note",
        ]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        asset = Asset.objects.filter(id=data.get("asset")).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not User.objects.filter(id=data.get("user")).exists():
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if asset.current_assignee or asset.status == "checked-out":
            return Response({"success": False, "info": "Asset already assigned"})

        # now = datetime.datetime.now().date()
        # data["request_date"] = now
        # print(now)

        data["submitted_by"] = request.user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset request added successfully"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[TokenRequiredPermission, AdminCheckPermission],
        url_path="asset-request-approval",
    )
    def asset_request_approval(self, request, *args, **kwargs):
        asset_request_id = request.data.get("asset_request")
        if not asset_request_id:
            return Response(
                {"success": False, "info": "Asset Request UID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request_status = request.data.get("status")

        if not request_status:
            return Response(
                {"success": False, "info": "Status not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request_status not in ["approved", "rejected"]:
            return Response(
                {"success": False, "info": "Invalid status provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset_request = get_object_or_404(AssetRequest, id=asset_request_id)

        if request_status == "approved":
            try:
                with transaction.atomic():
                    asset = asset_request.asset
                    asset.status = AssetStatus.objects.get(name="deployed")
                    asset.current_assignee = asset_request.user
                    asset.requestable = False
                    asset.save(
                        update_fields=["status", "current_assignee", "requestable"]
                    )

                    AssetAssignment.objects.create(
                        asset=asset_request.asset,
                        user=asset_request.user,
                        approved_by=request.user,
                    )

                    asset_request.status = "approved"
                    asset_request.approval_date = datetime.datetime.now().date()
                    asset_request.save(update_fields=["status", "approval_date"])

                return Response(
                    {"success": True, "info": "Asset request approved successfully"},
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "info": "Failed to approve asset request: " + str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        elif request_status == "rejected":
            asset_request.status = "rejected"
            asset_request.rejection_date = datetime.datetime.now().date()
            asset_request.save(update_fields=["status", "rejection_date"])
            return Response(
                {"success": True, "info": "Asset request rejected successfully"},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"success": False, "info": "Invalid status provided"},
                status=status.HTTP_400_BAD_REQUEST,
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

        asset = Asset.objects.filter(id=data.get("asset")).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = request.user.id
        data["user"] = user_id
        user = User.objects.filter(id=user_id)

        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset return added successfully"},
            status=status.HTTP_201_CREATED,
        )


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = AssetMaintenanceRequest.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetMaintenanceRequestCreateUpdateSerializer
        return AssetMaintenanceRequestListSerializer

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

        asset = Asset.objects.filter(id=data.get("asset")).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = request.user.id
        data["user"] = user_id

        user = User.objects.get(id=user_id)

        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # asset.status = AssetStatus.objects.get(name="out-for-repair")
        # asset.save(update_fields=['status'])

        data["report_date"] = datetime.datetime.now().date()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Maintenance request added successfully"},
            status=status.HTTP_201_CREATED,
        )


class AssetSupplierViewSet(viewsets.ModelViewSet):
    queryset = AssetSupplier.objects.all()
    permission_classes = [TokenRequiredPermission, AdminCheckPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in []:
            return AssetSupplierCreateUpdateSerializer
        return AssetSupplierListSerializer

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
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not phone:
            return Response(
                {"success": False, "info": "phone is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not address:
            return Response(
                {"success": False, "info": "address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AssetCheckInViewset(viewsets.ModelViewSet):
    queryset = AssetCheckIn.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCheckInCreateUpdateSerializer
        return AssetCheckInListSerializer

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
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(f"Error creating asset manufacturer: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
