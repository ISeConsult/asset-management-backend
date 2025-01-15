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
    AssetCheckOut,
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
    AssetCheckOut,
    Components,
    ComponentCheckIn,
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
    AssetManufacturerListSerializer,
    AssetModelCreateUpdateSerializer,
    AssetModelListSerializer,
    AssetLocationSerializer,
    AssetLocationListSerializer,
    CompanyCreateUpdateSerializer,
    AssetCheckInCreateUpdateSerializer,
    AssetCheckInListSerializer,
    AssetCheckoutListSerializer,
    AssetCheckOutCreateUpdateSerializer,
    AssetCreateUpdateSerializer,
    AssetListSerializer,
    AssetRequestCreateUpdateSerializer,
    AssetRequestListSerializer,
    AssetStatusSerializer,
    AssetReturnCreateUpdateSerializer,
    AssetReturnListSerializer,
    CompanyListSerializer,
    ComponentsCreateUpdateSerializer,
    ComponentsListSerializer,
    ComponentCheckInCreateUpdateSerializer,
    ComponentCheckInListSerializer,
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
    pagination_class = FetchDataPagination
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetManufacturerSerializer
        return AssetManufacturerListSerializer

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
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetLocationSerializer
        return AssetLocationListSerializer

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


class AssetViewset(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    permission_classes = [TokenRequiredPermission]
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

        asset_status = AssetStatus.objects.filter(name='pending').first()

        data['status'] = asset_status.id

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

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="requestable-assets",
        pagination_class=FetchDataPagination,
    )
    def fetch_requestable_assets(self, request, *args, **kwargs):
        try:
            assets = Asset.objects.filter(status__name="checked_in")

            # if not assets.exists():
            #     return Response(
            #         {'success': False, 'info': 'No assets found'},
            #         status=status.HTTP_404_NOT_FOUND
            #     )

            # Handle pagination
            page = self.paginate_queryset(assets)
            if page is not None:
                serializer = AssetListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # If pagination is not applied
            serializer = AssetListSerializer(assets, many=True)
            return Response(
                {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Error fetching requestable assets")
            return Response(
                {
                    "success": False,
                    "info": "An error occurred while processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="requested-assets",
        pagination_class=FetchDataPagination,
    )
    def fetch_requested_assets(self, request, *args, **kwargs):
        try:
            assets = AssetRequest.objects.all()

            # if not assets.exists():
            #     return Response(
            #         {'success': False, 'info': 'No assets found'},
            #         status=status.HTTP_404_NOT_FOUND
            #     )

            # Handle pagination
            page = self.paginate_queryset(assets)
            if page is not None:
                serializer = AssetRequestListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # If pagination is not applied
            serializer = AssetRequestListSerializer(assets, many=True)
            return Response(
                {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Error fetching requested assets")
            return Response(
                {
                    "success": False,
                    "info": "An error occurred while processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="issued-assets",
        pagination_class=FetchDataPagination,
    )
    def fetched_checked_out_assets(self, request, *args, **kwargs):
        try:
            assets = Asset.objects.filter(status__name="checked_out")

            # if not assets.exists():
            #     return Response(
            #         {'success': False, 'info': 'No assets found'},
            #         status=status.HTTP_404_NOT_FOUND
            #     )

            page = self.paginate_queryset(assets)
            if page is not None:
                serializer = AssetListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = AssetListSerializer(assets, many=True)
            return Response(
                {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Error fetching issued assets")
            return Response(
                {
                    "success": False,
                    "info": "An error occurred while processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class AssetRequestViewSet(viewsets.ModelViewSet):
    queryset = AssetRequest.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetRequestCreateUpdateSerializer
        return AssetRequestListSerializer

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
        required_fields = [
            "user",
            "asset",
            "note",
            "location",
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

        if not AssetLocation.objects.filter(id=data.get("location")).exists():
            return Response(
                {"success": False, "info": "Asset location does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if asset.current_assignee or asset.status.name == "checked_out":
            return Response(
                {"success": False, "info": "Asset already assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.datetime.now().date()
        data["request_date"] = now
        print(now)

        data["submitted_by"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Asset request added successfully"},
            status=status.HTTP_201_CREATED,
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
        required_fields = ["asset", "location"]

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
        data["return_date"] = arrow.now().date()
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
        required_fields = ["asset", "location"]

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

        loca = AssetLocation.objects.filter(id=data.get("location"))

        if not loca.exists():
            return Response(
                {"success": False, "info": "asset location does not exist"},
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

        stat = AssetStatus.objects.get(name="in_repair")
        if not stat:
            return Response(
                {"success": False, "info": "status not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset.status = stat
        asset.save(update_fields=["status"])

        data["request_date"] = datetime.datetime.now().date()

        maint = AssetMaintenanceRequest.objects.filter(user=user, asset=asset).exists()
        if maint:
            return Response(
                {"success": False, "info": "Maintenace already made"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Maintenance request added successfully"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[TokenRequiredPermission],
        url_path="maintenance-return",
    )
    def return_from_maintenance(self, request, *args, **kwargs):
        try:
            data = request.data
            m_request = data.get("maintenace")

            if not m_request:
                return Response(
                    {"success": False, "info": "maintenance request not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            maintenance_request = AssetMaintenanceRequest.objects.filter(
                id=m_request, status="pending"
            ).first()

            if not maintenance_request:
                return Response(
                    {"success": False, "info": "maintenace request not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            stat = AssetStatus.objects.filter(name="checked_out").first()
            if not stat:
                return Response(
                    {"success": False, "info": "Status not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            maintenance_request.asset.status = stat
            maintenance_request.asset.save(update_fields=["status"])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"success": True, "info": "Maintenace request updated sucessfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AssetSupplierViewSet(viewsets.ModelViewSet):
    queryset = AssetSupplier.objects.all()
    permission_classes = [TokenRequiredPermission]
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
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCheckInCreateUpdateSerializer
        return AssetCheckInListSerializer

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

        asset = data.get("asset")
        location = data.get("location")

        if not asset:
            return Response(
                {"success": False, "info": "asset is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not location:
            return Response(
                {"success": False, "info": "location is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset = Asset.objects.filter(id=asset).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location = AssetLocation.objects.filter(id=location).first()

        if not location:
            return Response(
                {"success": False, "info": "Asset location does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["checkin_date"] = arrow.now().date()
        data["user"] = request.user.id

        asset_status = AssetStatus.objects.filter(name="checked_in").first()
        if not asset_status:
            return Response(
                {"success": False, "info": "Asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset.status = asset_status
        asset.save(update_fields=["status"])

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


class AssetCheckoutViewset(viewsets.ModelViewSet):
    queryset = AssetCheckOut.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AssetCheckOutCreateUpdateSerializer
        return AssetCheckoutListSerializer

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
        asset_request = data.get("asset_request")
        request_status = data.get("request_status")

        if not asset_request:
            return Response(
                {"success": False, "info": "asset request is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ass_request = AssetRequest.objects.filter(id=asset_request).first()

        if not ass_request:
            return Response(
                {"success": False, "info": "Asset request does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["checkout_by"] = request.user.id

        data["user"] = ass_request.user.id

        asset_status = AssetStatus.objects.get(name="checked_out")
        if not asset_status:
            return Response(
                {"success": False, "info": "Asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request_status == "approved":
            ass_request.status = "approved"
            ass_request.asset.current_assignee = ass_request.user
            ass_request.asset.status = asset_status
            ass_request.asset.save(update_fields=["current_assignee", "status"])
            ass_request.save(update_fields=["status"])

        else:
            ass_request.status = "rejected"
            ass_request.save(update_fields=["status"])

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


class ComponentsViewset(viewsets.ModelViewSet):
    queryset = Components.objects.all()
    lookup_field = "uid"
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ComponentsCreateUpdateSerializer
        return ComponentsListSerializer

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
        description = data.get("description")
        category = data.get("category")
        manufacturer = data.get("manufacturer")
        model = data.get("model")
        location = data.get("location")
        component_status = data.get("status")
        purchase_date = data.get("purchase_date")
        purchase_cost = data.get("purchase_cost")
        supplier = data.get("supplier")
        item_number = data.get("item_number")

        if not item_number:
            return Response(
                {"success": False, "info": "item_number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not description:
            return Response(
                {"success": False, "info": "description is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not category:
            return Response(
                {"success": False, "info": "category is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not manufacturer:
            return Response(
                {"success": False, "info": "manufacturer is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            return Response(
                {"success": False, "info": "model is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not location:
            return Response(
                {"success": False, "info": "location is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not component_status:
            return Response(
                {"success": False, "info": "status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not purchase_date:
            return Response(
                {"success": False, "info": "purchase_date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not purchase_cost:
            return Response(
                {"success": False, "info": "purchase_cost is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not supplier:
            return Response(
                {"success": False, "info": "supplier is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cat = AssetCategory.objects.filter(id=category).first()
        if not cat:
            return Response(
                {"success": False, "info": "category does not exist"},
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

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[TokenRequiredPermission],
        url_path="checkout-components",
    )
    def check_out_component(self, request, *args, **kwargs):
        try:
            data = request.data
            component = data.get("component")
            user = data.get("user")

            if not component:
                return Response(
                    {"success": False, "info": "component is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user:
                return Response(
                    {"success": False, "info": "user is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            component = Components.objects.filter(id=component).first()
            if not component:
                return Response(
                    {"success": False, "info": "component not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if component.status.name != "checked_in":
                return Response(
                    {
                        "success": False,
                        "info": "Component is not available for checkout",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(id=user).first()
            if not user:
                return Response(
                    {"success": False, "info": "user not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            component_status = AssetStatus.objects.filter(name="checked_out").first()
            if not component_status:
                return Response(
                    {"success": False, "info": "status not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            component.status = component_status
            component.current_assignee = user
            component.save(update_fields=["status", "current_assignee"])

            return Response(
                {"success": True, "info": "Component checked out successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ComponentCheckInViewset(viewsets.ModelViewSet):
    queryset = ComponentCheckIn.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ComponentCheckInCreateUpdateSerializer
        return ComponentCheckInListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "info": serializer.data})
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = data.get("user")
            component = data.get("component")
            location = data.get("location")
            
            
            if not user:
                return Response(
                    {"success": False, "info": "user is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not component:
                return Response(
                    {"success": False, "info": "component is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not location:
                return Response(
                    {"success": False, "info": "location is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            component = Components.objects.filter(id=component).first()
            if not component:
                return Response(
                    {"success": False, "info": "Component not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            user = User.objects.filter(id=user).first()
            if not user:
                return Response(
                    {"success": False, "info": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            location = AssetLocation.objects.filter(id=location).first()
            if not location:
                return Response(
                    {"success": False, "info": "Location not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            component_status = AssetStatus.objects.filter(name="checked_in").first()

            data['checkin_date'] = arrow.now().date()
            component.status = component_status
            component.save(update_fields=["status"])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"success": True, "info": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    

