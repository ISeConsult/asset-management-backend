from django.urls import path, include

# from apps.assets.views import (

# )

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
]
