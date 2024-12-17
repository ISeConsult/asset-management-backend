from django.shortcuts import render
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

from apps.licence.models import (
  LicenseCategoryTypes,
  LicenseCategory,
  License,
  LicenseCheckOut
)

from apps.licence.serializers import (
    LicenseCategoryTypesSerializer,
    LicenseCategoryCreateUpdateSerializer,
    LicenseCategoryListSerializer,
    LicenseCreateUpdateSerializer,
    LicenseListSerializer,
    LicenseCheckOutCreateUpdateSerializer,
    LicenseCheckOutListSerializer
)

logger = logging.getLogger(__name__)

# Create your views here.



class LicenseCategoryTypesViewset(viewsets.ModelViewSet):
    queryset = LicenseCategoryTypes.objects.all()
    permission_classes = [TokenRequiredPermission]
    serializer_class = LicenseCategoryTypesSerializer
    lookup_field = 'uid'

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
            logger.warning(f"Error creating License Category Types: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        


class LicenseCategoryViewset(viewsets.ModelViewSet):
    queryset = LicenseCategory.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.action in ['create',"update","partial_update"]:
            return LicenseCategoryCreateUpdateSerializer
        return LicenseCategoryListSerializer
    
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
        category_type = data.get('category_type')

        if not name:
            return Response(
                {
                    "success": False,
                    "info": "name is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not category_type:
            return Response(
                {
                    "success": False,
                    "info": "category_type is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        cat_type = LicenseCategoryTypes.objects.filter(id=category_type).first()

        if not cat_type:
            return Response(
                {
                    "success": False,
                    "info": "LicenseCategoryType Does not exist",
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
            logger.warning(f"Error creating License Category Types: {str(e)}")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        


class LicenseViewset(viewsets.ModelViewSet):
    queryset = License.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = 'uid'
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return LicenseCreateUpdateSerializer
        return LicenseListSerializer
    
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
        name = data.get('name')
        product_key = data.get('product_key')
        category = data.get('category')
        

    

    

    


