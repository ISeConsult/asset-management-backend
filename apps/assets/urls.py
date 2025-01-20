from django.urls import path, include

from apps.assets.views import (
    AssetCategoryViewSet,
    AssetManufacturerViewset,
    AssetLocationViewset,
    CompanyViewset,
    AssetModelViewset,
    AssetModelCategoryViewset,
    AssetStatusViewSet,
    AssetViewset,
    AssetRequestViewSet,
    AssetReturnViewSet,
    MaintenanceRequestViewSet,
    AssetSupplierViewSet,
    AssetCategoryTypesViewset,
    AssetCheckInViewset,
    AssetCheckoutViewset,
    ComponentsViewset,
    ComponentCheckInViewset,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r"asset-category-type", AssetCategoryTypesViewset, basename="asset-category-type"
)
router.register(r"asset-category", AssetCategoryViewSet, basename="asset-category")
router.register(
    r"asset-manufacturer", AssetManufacturerViewset, basename="asset-manufacturer"
)
router.register(r"asset-location", AssetLocationViewset, basename="asset-location")
router.register(r"company", CompanyViewset, basename="company")
router.register(r"asset-model", AssetModelViewset, basename="asset-model")
router.register(
    r"assetmodel-category", AssetModelCategoryViewset, "assetmodel-category"
)
router.register(r"asset-status", AssetStatusViewSet, "asset-status")    
router.register(r"assets", AssetViewset, basename="assets")
router.register(r"asset-request", AssetRequestViewSet, "asset-request")
router.register(r"asset-check-in", AssetCheckInViewset, basename="asset-check-in")
router.register(r"asset-check-out", AssetCheckoutViewset, basename="asset-check-out")
router.register(r"asset-return", AssetReturnViewSet, basename="asset-return")
router.register(
    r"maitenance-request", MaintenanceRequestViewSet, basename="maintenance-request"
)
router.register(r"asset-supplier", AssetSupplierViewSet, "asset-supplier")
router.register(r"components", ComponentsViewset, "components")
router.register(r'component-check-in', ComponentCheckInViewset, 'component-check-in')

urlpatterns = [
    path("", include(router.urls)),
]
