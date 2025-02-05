from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.userActivities.views import UserActivityListViewset

router = DefaultRouter()


urlpatterns = [
    path(
        "user-activities/", UserActivityListViewset.as_view(), name="user-activity-list"
    ),
]
