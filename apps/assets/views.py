import datetime
import logging
import arrow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction
from apps.assets.pagination import FetchDataPagination
from apps.licence.models import License
from apps.licence.serializers import LicenseListSerializer
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
    ComponentRequest,
    ComponentCheckOut,
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
    ComponentCheckOutCreateUpdateSerializer,
    ComponentCheckOutListSerializer,
    ComponentsCreateUpdateSerializer,
    ComponentsListSerializer,
    ComponentCheckInCreateUpdateSerializer,
    ComponentCheckInListSerializer,
    ComponentRequestCreateUpdateSerializer,
    ComponentRequestListSerializer,
)
from apps.people.serializers import UserListSerializer
from django.db import transaction
from rest_framework.exceptions import ValidationError

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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="category-detail",
    )
    def get_category_details(self, request, *args, **kwargs):
        try:
            cat_id = kwargs.get("uid")

            if not cat_id:
                return Response(
                    {"success": False, "info": "Category UID not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch assets under the category
            assets = Asset.objects.filter(category__uid=cat_id)
            asset_serializer = AssetListSerializer(assets, many=True).data

            # Fetch asset models associated with the category
            asset_models = AssetModel.objects.filter(
                asset__category__uid=cat_id
            ).distinct()
            asset_model_serializer = AssetModelListSerializer(
                asset_models, many=True
            ).data

            # Prepare the final response
            return Response(
                {
                    "success": True,
                    "info": {
                        "assets": asset_serializer,
                        "asset_models": asset_model_serializer,
                    },
                }
            )

        except Exception as e:
            logger.warning(f"Error in get_category_details: {str(e)}")
            return Response(
                {
                    "success": False,
                    "info": "An error occurred while processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AssetManufacturerViewset(viewsets.ModelViewSet):
    queryset = AssetManufacturer.objects.all()
    permission_classes = [TokenRequiredPermission]
    pagination_class = FetchDataPagination
    lookup_field = "uid"

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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="manufacturer-detail",
    )
    def get_manufacturer_details(self, request, *args, **kwargs):
        try:
            man_id = kwargs.get("uid")

            if not man_id:
                return Response(
                    {"success": False, "info": "Manufacturer's uid not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            assets = Asset.objects.select_related("manufacturer").filter(
                manufacturer__uid=man_id
            )
            ass_serializer = AssetListSerializer(assets, many=True).data

            accessories = assets.filter(category__name="accessories")
            acc_serializer = AssetListSerializer(accessories, many=True).data

            consumables = assets.filter(category__name="consumables")
            con_serializer = AssetListSerializer(consumables, many=True).data

            comp = Components.objects.filter(manufacturer__uid=man_id)
            component = ComponentsListSerializer(comp, many=True).data

            return Response(
                {
                    "success": True,
                    "info": {
                        "assets": ass_serializer,
                        "consumables": con_serializer,
                        "accessories": acc_serializer,
                        "components": component,
                    },
                }
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="location-detail",
    )
    def get_location_details(self, request, *args, **kwargs):
        try:
            location_id = kwargs.get("uid")

            if not location_id:
                return Response(
                    {"success": False, "info": "location_id not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            asset = Asset.objects.filter(location__uid=location_id)
            asset_data = AssetListSerializer(asset, many=True).data

            accessories = asset.filter(category__name="accessories")
            acc_serializer = AssetListSerializer(accessories, many=True).data

            consumables = asset.filter(category__name="consumables")
            con_serializer = AssetListSerializer(consumables, many=True).data

            comp = Components.objects.filter(location__uid=location_id)
            component = ComponentsListSerializer(comp, many=True).data

            user_data = User.objects.filter(location__uid=location_id)
            users = UserListSerializer(user_data, many=True).data

            return Response(
                {
                    "success": True,
                    "info": {
                        "assets": asset_data,
                        "accessories": acc_serializer,
                        "consumables": con_serializer,
                        "components": component,
                        "users": users,
                    },
                }
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="company-detail",
    )
    def company_details(self, request, *args, **kwargs):
        try:
            company_id = kwargs.get("uid")

            if not company_id:
                return Response(
                    {"success": False, "info": "Company UID not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            asset = Asset.objects.filter(company__uid=company_id)
            asset_data = AssetListSerializer(asset, many=True).data

            accessories = asset.filter(category__name="accessories")
            acc_serializer = AssetListSerializer(accessories, many=True).data

            consumables = asset.filter(category__name="consumables")
            con_serializer = AssetListSerializer(consumables, many=True).data

            comp = Components.objects.filter(company__uid=company_id)
            component = ComponentsListSerializer(comp, many=True).data

            user_data = User.objects.filter(department__company__uid=company_id)
            users = UserListSerializer(user_data, many=True).data

            lisc = License.objects.filter(company__uid=company_id)
            licenses = LicenseListSerializer(lisc, many=True).data

            return Response(
                {
                    "success": True,
                    "info": {
                        "assets": asset_data,
                        "accessories": acc_serializer,
                        "consumables": con_serializer,
                        "components": component,
                        "licenses": licenses,
                        "users": users,
                    },
                }
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="asset-model-detail",
    )
    def list_assets_under_Assetmodel(self, request, *args, **kwargs):
        try:
            print(f"uid {kwargs.get('uid')}")
            model_id = kwargs.get("uid")

            if not model_id:
                return Response(
                    {"success": False, "info": "Model ID not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            asset = Asset.objects.filter(asset_model__uid=model_id)

            serializer = AssetListSerializer(asset, many=True).data

            return Response(
                {"success": True, "info": serializer},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

        if AssetStatus.objects.filter(name=name).exists():
            return Response(
                {
                    "success": False,
                    "info": "Asset status already exists",
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

        asset_status = AssetStatus.objects.filter(name="pending").first()

        data["status"] = asset_status.id

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
        required_fields = ["asset", "note"]

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

        if asset.current_assignee or asset.status.name == "checked_out":
            return Response(
                {"success": False, "info": "Asset already assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.datetime.now().date()
        data["request_date"] = now
        data["user"] = request.user.id
        data["location"] = asset.location.id
        print(now)

        data["submitted_by"] = request.user.id

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
        permission_classes=[TokenRequiredPermission],
        url_path="cancel-request",
    )
    def cancel_request(self, request, *args, **kwargs):
        try:
            data = request.data
            aset_request = data.get("asset_request")
            note = data.get("note")

            if not aset_request:
                return Response(
                    {"success": False, "info": "asset_request is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not note:
                return Response(
                    {"success": False, "info": "note is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            asset_request = AssetRequest.objects.filter(id=aset_request).first()

            if not asset_request:
                return Response(
                    {"success": False, "info": "Asset request does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            asset_request.status = "rejected"
            asset_request.note = note
            asset_request.save(update_fields=["status", "note"])

            return Response(
                {"success": True, "info": "Asset request cancelled successfully"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.warning(f"Error cancelling asset request: {str(e)}")
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                },
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
        datas = request.data
        data = datas.copy()
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

        data['location'] = asset.location.id
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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[TokenRequiredPermission],
        url_path="supplier-details",
    )
    def get_suplier_details(self, request, *args, **kwargs):
        try:

            supply_id = kwargs.get("uid")

            if not supply_id:
                return Response({"success": "Suplier_id not found"})

            asset_data = Asset.objects.filter(supplier__uid=supply_id)
            asset = AssetListSerializer(asset_data, many=True).data

            comp = Components.objects.filter(supplier__uid=supply_id)
            components = ComponentsListSerializer(comp, many=True).data

            consu = asset_data.filter(category__name="consumables")
            consumables = AssetListSerializer(consu, many=True).data

            acc_data = asset_data.filter(category__name="accessories")
            accessories = AssetListSerializer(acc_data, many=True).data

            return Response(
                {
                    "success": True,
                    "info": {
                        "assets": asset,
                        "components": components,
                        "consumables": consumables,
                        "accessories": accessories,
                    },
                }
            )

        except Exception as e:
            logger.warning(str(e))
            return Response(
                {
                    "success": False,
                    "info": "An error occured whilst processing your request",
                }
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

        if not asset:
            return Response(
                {"success": False, "info": "asset is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset = Asset.objects.filter(id=asset).first()

        if not asset:
            return Response(
                {"success": False, "info": "Asset does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["location"] = asset.location.id

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
        asset_request_id = data.get("asset_request")
        user_id = data.get("user")
        asset_id = data.get("asset")

        if asset_request_id:
            try:
                asset_request = AssetRequest.objects.get(id=asset_request_id)
                asset = asset_request.asset
                
            except AssetRequest.DoesNotExist:
                return Response(
                    {"success": False, "info": "Asset request does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )   

            data["asset"] = asset_request.asset.id
            data['user'] = asset_request.user.id

            # Ensure the asset is associated with the asset request
            assets = asset_request.asset
            if not assets:
                return Response(
                    {
                        "success": False,
                        "info": "No asset is associated with this asset request",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update asset request status to approved
            asset_request.status = "approved"
            asset_request.save(update_fields=["status"])
        else:
            # If no asset request, validate the asset is passed in the request body
            if not asset_id:
                return Response(
                    {
                        "success": False,
                        "info": "Asset ID is required when no asset request is provided",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not user_id:
                return Response(
                    {"success": False, "info": "User ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                asset = Asset.objects.get(id=asset_id)
                data["asset"] = asset_id
                data['user'] = user_id
            except Asset.DoesNotExist:
                return Response(
                    {"success": False, "info": "Asset does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            asset_status = AssetStatus.objects.get(name="checked_out")
        except AssetStatus.DoesNotExist:
            return Response(
                {"success": False, "info": "Asset status does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset.status = asset_status
        asset.current_assignee = user

        with transaction.atomic():
            asset.save(update_fields=["status", "current_assignee"])
            data["checkout_by"] = request.user.id

            serializer = self.get_serializer(data=data)

            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"success": True, "info": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response(
                    {"success": False, "error": e.detail},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logger.warning(f"Error creating asset checkout: {str(e)}")
                return Response(
                    {"success": False, "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
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
        category = data.get("category")
        manufacturer = data.get("manufacturer")
        model = data.get("model")
        location = data.get("location")
        component_status = data.get("status")
        purchase_date = data.get("purchase_date")
        purchase_cost = data.get("purchase_cost")
        supplier = data.get("supplier")
        # item_number = data.get("item_number")

        # if not item_number:
        #     return Response(
        #         {"success": False, "info": "item_number is required"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        if not name:
            return Response(
                {"success": False, "info": "name is required"},
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
            component = data.get("component")

            if not component:
                return Response(
                    {"success": False, "info": "component is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


            component = Components.objects.filter(id=component).first()
            if not component:
                return Response(
                    {"success": False, "info": "Component not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            component_status = AssetStatus.objects.filter(name="checked_in").first()

            data["checkin_date"] = arrow.now().date()
            data['user'] = request.user.id
            data['location'] = component.location.id
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


class ComponentRequestViewset(viewsets.ModelViewSet):
    queryset = ComponentRequest.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ComponentRequestCreateUpdateSerializer
        return ComponentRequestListSerializer
    
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
        data = request.data
        required_fields = ["component", "note"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        component = Components.objects.filter(id=data.get("component")).first()

        if not component:
            return Response(
                {"success": False, "info": "Component does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if component.current_assignee or component.status.name == "checked_out":
            return Response(
                {"success": False, "info": "Component already assigned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime.datetime.now().date()
        data["request_date"] = now
        data["user"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "Component request added successfully"},
            status=status.HTTP_201_CREATED,
        )


class ComponentCheckoutViewset(viewsets.ModelViewSet):
    queryset = ComponentCheckOut.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ComponentCheckOutCreateUpdateSerializer
        return ComponentCheckOutListSerializer
    
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
            component_request_id = data.get('component_request')
            component_id = data.get('component')
            user_id = data.get('user')

            # Validate at least one identifier is provided
            if not component_request_id and not component_id:
                return Response(
                    {"success": False, "info": "Component request ID or component ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            component = None  # Initialize to avoid unassigned variable error

            if component_request_id:
                try:
                    component_request = ComponentRequest.objects.get(id=component_request_id)
                    data["component"] = component_request.component.id
                    data["user"] = component_request.user.id

                    # Ensure the component is associated
                    if not component_request.component:
                        return Response(
                            {"success": False, "info": "No component associated with this request"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Update request status
                    component_request.status = "approved"
                    component_request.save(update_fields=["status"])
                    component = component_request.component

                except ComponentRequest.DoesNotExist:
                    return Response(
                        {"success": False, "info": "Component request does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif component_id:
                if not user_id:
                    return Response(
                        {"success": False, "info": "User ID is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    component = Components.objects.get(id=component_id)
                    user = User.objects.get(id=user_id)
                    component_status = AssetStatus.objects.get(name="checked_out")

                    component.status = component_status
                    component.current_assignee = user
                    data["component"] = component_id
                    data["user"] = user_id

                except Components.DoesNotExist:
                    return Response(
                        {"success": False, "info": "Component does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except User.DoesNotExist:
                    return Response(
                        {"success": False, "info": "User does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except AssetStatus.DoesNotExist:
                    return Response(
                        {"success": False, "info": "Component status does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            with transaction.atomic():
                # Save component updates if component is assigned
                if component:
                    component.save(update_fields=["status", "current_assignee"])
                else:
                    return Response(
                        {"success": False, "info": "Component could not be processed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                data["checkout_by"] = request.user.id

                # Serialize and save checkout
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(
                    {"success": True, "info": serializer.data},
                    status=status.HTTP_201_CREATED,
                )

        except ValidationError as e:
            return Response(
                {"success": False, "error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return Response(
                {"success": False, "info": "An error occurred while processing your request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
