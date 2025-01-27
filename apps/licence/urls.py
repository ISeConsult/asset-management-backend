from django.urls import path,include
from rest_framework.routers import DefaultRouter
from apps.licence.views import (
    LicenseCategoryTypesViewset,
    LicenseCategoryViewset,
    LicenseViewset,
    LicenseCheckoutViewset,
    LicenseHistoryViewset
)

router = DefaultRouter()
router.register(r"license-category-type",LicenseCategoryTypesViewset,basename='license-category-type')
router.register(r"license-category",LicenseCategoryViewset,basename="license-category")
router.register(r"license",LicenseViewset,basename='license')
router.register(r'license-checkout',LicenseCheckoutViewset,basename='license-checkout')
router.register(r"license-history",LicenseHistoryViewset,basename='license-history')




urlpatterns = [
    path('',include(router.urls))
]