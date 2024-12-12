from django.urls import path,include
from apps.assets.views import (
    AssetCategoryViewSet,
    AssetStatusViewSet,
    SoftwareCategoryViewSet,
    AssetViewset,
    AssetRequestViewSet,
    AssetAssignmentViewSet,
    AssetReturnViewSet,
    MaintenanceRequestViewSet,
    AssetSupplierViewSet,
    SoftwareLicencesViewSet,
    LicenceCheckoutViewset,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'asset-categories', AssetCategoryViewSet)
router.register(r'asset-status', AssetStatusViewSet)
router.register(r'software-categories', SoftwareCategoryViewSet)
router.register(r'assets', AssetViewset)
router.register(r'asset-requests', AssetRequestViewSet)
router.register(r'asset-assignments', AssetAssignmentViewSet)
router.register(r'asset-returns', AssetReturnViewSet)
router.register(r'maintenance-requests', MaintenanceRequestViewSet)
router.register(r'asset-suppliers', AssetSupplierViewSet)
router.register(r'software-licences', SoftwareLicencesViewSet)
router.register(r'licence-checkouts', LicenceCheckoutViewset)

urlpatterns = [
    path('', include(router.urls)),
]