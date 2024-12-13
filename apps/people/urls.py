from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.people.views import UserViewset, DepartmentViewset, RoleViewset

router = DefaultRouter()
router.register(r"users", UserViewset)
router.register(r"departments", DepartmentViewset)
router.register(r"roles", RoleViewset)


urlpatterns = [
    path("", include(router.urls)),
]
