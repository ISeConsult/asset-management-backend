from django.shortcuts import render
import datetime
import logging
import arrow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from django.db import transaction
from apps.assets.pagination import FetchDataPagination
from apps.people.models import User
from apps.people.permissions import TokenRequiredPermission, AdminCheckPermission
from apps.userActivities.models import UserActivity
from apps.userActivities.serializers import UserActivitiesSerializer


# Create your views here.


class UserActivityListViewset(generics.ListAPIView):
    queryset = UserActivity.objects.select_related("user").all()
    serializer_class = UserActivitiesSerializer
    permission_classes = [TokenRequiredPermission]
    pagination_class = FetchDataPagination
    filterset_fields = ["user__id", "created_at"]
    search_fields = ["user__fullname", "activity_type"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]  # Default ordering
