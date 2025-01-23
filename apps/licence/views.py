from django.shortcuts import render
import datetime
import logging
import arrow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction
from apps.assets.models import AssetManufacturer
from apps.assets.pagination import FetchDataPagination
from apps.people.models import User
from apps.people.permissions import TokenRequiredPermission, AdminCheckPermission

from apps.licence.models import (
  LicenseCategoryTypes,
  LicenseCategory,
  License,
  LicenseCheckOut,
    LicenseHistory,
)

from apps.licence.serializers import (
    LicenseCategoryTypesSerializer,
    LicenseCategoryCreateUpdateSerializer,
    LicenseCategoryListSerializer,
    LicenseCreateUpdateSerializer,
    LicenseListSerializer,
    LicenseCheckOutCreateUpdateSerializer,
    LicenseCheckOutListSerializer,
    LicenseHistoryCreateUpdateSerializer,
    LicenseHistoryListSerializer,
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
        try:
            data = request.data
            name = data.get('name')
            product_key = data.get('product_key')
            category = data.get('category')
            manufacturer = data.get('manufacturer')
            order_number = data.get('order_number')
            # licensed_to = data.get('licensed_to')
            purchase_cost = data.get('purchase_cost')
            expiry_date = data.get('expiry_date')
            purchase_date = data.get('purchase_date')


            if not name:
                return Response(
                    {
                        "success": False,
                        "info": "name is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not product_key:
                return Response(
                    {
                        "success": False,
                        "info": "product_key is required",
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
            
            if not order_number:
                return Response(
                    {
                        "success": False,
                        "info": "order_number is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # if not licensed_to:
            #     return Response(
            #         {
            #             "success": False,
            #             "info": "licensed_to is required",
            #         },
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            
            if not purchase_cost:
                return Response(
                    {
                        "success": False,
                        "info": "purchase_cost is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not expiry_date:
                return Response(
                    {
                        "success": False,
                        "info": "expiry_date is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not purchase_date:
                return Response(
                    {
                        "success": False,
                        "info": "purchase_date is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            categ = LicenseCategory.objects.filter(id=category).first()
            if not categ:
                return Response(
                    {
                        "success": False,
                        "info": "License Category does not exist",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            manu = AssetManufacturer.objects.filter(id=manufacturer).first()
            if not manu:
                return Response(
                        {
                            "success": False,
                            "info": "License Manufacturer does not exist",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    ) 
            
            # lic_to = User.objects.filter(id=licensed_to).first()
            # if not lic_to:
            #     return Response(
            #         {
            #             "success": False,
            #             "info": "Licensed to User  does not exist",
            #         },
            #         status=status.HTTP_400_BAD_REQUEST,
            #     ) 
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'success':True,'info':"License Created Successfully"},status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.warning(str(e))
            return Response({'success':False,'info':"An error occured whilst processing your request"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        

class LicenseCheckoutViewset(viewsets.ModelViewSet):
    queryset = LicenseCheckOut.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.action in ["create","update","partial_update"]:
            return LicenseCheckOutCreateUpdateSerializer
        return LicenseCheckOutListSerializer
    
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
        try:
            data = request.data
            license = data.get('license')
            user = data.get('user')

            if not license:
                return Response({'success':False,'info':'license is required'},status=status.HTTP_400_BAD_REQUEST)
            
            if not user:
                return Response({'success':False,'info':'user is required'},status=status.HTTP_400_BAD_REQUEST)
            
            lisc = License.objects.filter(id=license).first()
            if not lisc:
                return Response({'success':False,'info':'license cannot be found'},status=status.HTTP_400_BAD_REQUEST)
            
            if lisc.licensed_to:
                return Response({'success':False,'info':'license has been checked out'},status=status.HTTP_400_BAD_REQUEST)
            
            user_data = User.objects.filter(id=user).first()

            if not user_data:
                Response({'success':False,'info':'User cannot be found'},status=status.HTTP_400_BAD_REQUEST)

            data["checkout_by"] = request.user.id

            lisc.licensed_to = user_data
            lisc.licensed_to_email = user_data.email
            lisc.status = 'checked_out'
            lisc.save(update_fields=['licensed_to','licensed_to_email','status'])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            LicenseHistory.objects.create(license=lisc,user=user_data,action='checked_out')

            return Response({'success':True,'info':'License Checked out successfully'},status=status.HTTP_201_CREATED)
            
        
        except Exception as e:
            logger.warning(str(e))
            return Response(
            {"success": True, "info": "An error occured whilst processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

        
class LicenseHistoryViewset(viewsets.ModelViewSet):
    queryset = LicenseHistory.objects.all()
    permission_classes = [TokenRequiredPermission]
    lookup_field = 'uid'
    pagination_class = FetchDataPagination

    def get_serializer_class(self):
        if self.action in ["create","update","partial_update"]:
            return LicenseHistoryCreateUpdateSerializer
        return LicenseHistoryListSerializer
    
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
        try:
            data = request.data
            license = data.get('license')
            user = data.get('user')
            action = data.get('action')
            note = data.get('note')

            if not license:
                return Response({'success':False,'info':'license is required'},status=status.HTTP_400_BAD_REQUEST)
            
            if not user:
                return Response({'success':False,'info':'user is required'},status=status.HTTP_400_BAD_REQUEST)
            
            if not action:
                return Response({'success':False,'info':'action is required'},status=status.HTTP_400_BAD_REQUEST)
            
            lisc = License.objects.filter(id=license).first()
            if not lisc:
                return Response({'success':False,'info':'license cannot be found'},status=status.HTTP_400_BAD_REQUEST)
            
            user_data = User.objects.filter(id=user).first()

            if not user_data:
                Response({'success':False,'info':'User cannot be found'},status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'success':True,'info':'License History Created successfully'},status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.warning(str(e))
            return Response(
            {"success": True, "info": "An error occured whilst processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )






    

    

    


