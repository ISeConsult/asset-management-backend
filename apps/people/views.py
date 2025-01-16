import arrow
from django.shortcuts import render
from apps.people.serializers import (
    UserCreateUpdateSerializer,
    UserListSerializer,
    RoleSerializer,
    DepartmentCreateUpdateSerializer,
    DepartmentListSerializer,
)
from apps.people.models import User, Role, Department
from apps.people.permissions import AdminCheckPermission, TokenRequiredPermission
from rest_framework import permissions, status, filters, viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes, action
from apps.people.utils import send_notification
from apps.people.auth import Authenticator
from apps.people.utils import send_login_credentials
import logging
# Create your views here.

logger = logging.getLogger(__name__)

auth = Authenticator()


class RoleViewset(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    #permission_classes = [AdminCheckPermission]
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
                {"success": False, "info": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_200_OK
        )


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    #permission_classes = [AdminCheckPermission]
    lookup_field = "uid"
    filter_backends = [filters.SearchFilter]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return DepartmentCreateUpdateSerializer
        return DepartmentListSerializer

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
        required_fields = ["name", "manager"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        dep = Department.objects.filter(name=data.get("name"))

        if dep.exists():
            return Response(
                {
                    "success": False,
                    "info": "Department already exists with the given name",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": serializer.data}, status=status.HTTP_201_CREATED
        )

    @action(detail=True,methods=['get'],permission_classes=[TokenRequiredPermission],url_path='department-details')
    def get_department_details(self,request,*args,**kwargs):
        try:
            department_id = kwargs.get('uid')

            if not department_id:
                return Response({'success':False,'info':'department_id was not provided'},status=status.HTTP_400_BAD_REQUEST)
 
            dept = Department.objects.filter(uid=department_id).first()

            users = User.objects.filter(department=dept)

            users_list =  UserListSerializer(users,many=True).data

            return Response({'success':True,'info':users_list})

        except Exception as e:
            logger.warning(str(e))
            return Response({'success':False,'info':'An error occured whilst processing your request'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    lookup_field = "uid"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateUpdateSerializer
        return UserListSerializer

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
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "department",
            "role",
            "phone",
            "employee_no",
        ]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "info": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if User.objects.filter(phone=data.get("phone")).exists():
            return Response(
                {
                    "success": False,
                    "info": "User already exists with the given phone number",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=data.get("email")).exists():
            return Response(
                {"success": False, "info": "User already exists with the given email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "info": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="update-password",
    )
    def update_password(self, request, pk=None):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not password:
            return Response(
                {"success": False, "info": "password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not confirm_password:
            return Response(
                {"success": False, "info": "confirm_password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                {"success": False, "info": "passwords do no match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        compare = check_password(password, user.password)

        if not compare:
            user.password = make_password(password)
            user.password_changed = True
            user.save(update_fields=["password", "password_changed"])
            return Response(
                {"success": True, "info": "passwords updated successfully"},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {
                    "success": False,
                    "info": "old password cannot be the same as new password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="forgot-password",
    )
    def forgot_password(self, request, pk=None):
        data = request.data
        email = data.get("email")
        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        mail = User.objects.filter(email=email).first()
        if not mail:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        auth.send_otp(email=email)

        return Response({"success": True, "info": "otp sent successfully"})

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="verify-otp",
    )
    def verify_otp(self, request, pk=None):
        data = request.data
        email = data.get("email")
        otp = data.get("otp")
        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not otp:
            return Response(
                {"success": False, "info": "otp is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify = auth.forgot_verify_otp(email=email, user_entered_otp=otp)

        return verify

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        url_path="login",
    )
    def login(self, request, pk=None):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        if not email:
            return Response(
                {"success": False, "info": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not password:
            return Response(
                {"success": False, "info": "password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"success": False, "info": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = arrow.now().datetime
        if not user.password_changed and user.password_expiry <= now:
            return Response(
                {
                    "success": False,
                    "info": "password expired. Contact your administrator",
                }
            )

        if not user.login_enabled:
            return Response(
                {"success": False, "info": "User login is disabled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        checker = check_password(password, user.password)
        if checker:
            token = auth.generate_token(email)
            if user.password_changed:
                return Response(
                    {
                        "success": True,
                        "info": "User logged in successfully",
                        "token": token,
                        "password_changed": True,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {
                        "success": True,
                        "info": "User logged in successfully, please change your password",
                        "token": token,
                        "password_changed": False,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response({"success": False, "info": "Invalid credentials"})
