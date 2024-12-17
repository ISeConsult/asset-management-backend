from rest_framework.permissions import BasePermission,SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
import jwt
import arrow
from decouple import config
import logging

from apps.assets.models import AssetRequest

logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model

User = get_user_model()


class TokenRequiredPermission(BasePermission):
    def has_permission(self, request, view):
        access_token = request.headers.get("Authorization")

        if not access_token:
            raise PermissionDenied("Auth token is missing.")

        try:
            decoded_token = jwt.decode(
                access_token, config("SECRET_KEY"), algorithms=["HS256"]
            )

            expiration_time = arrow.get(decoded_token["exp"])
            logger.warning(expiration_time)

            # Set the user on the request
            decoded_token.get("user_id")
            logged_user = User.objects.get(id=decoded_token.get("user_id"))
            if logged_user:
                request.user = logged_user

                print(f"Logged in user: {request.user}")

            else:
                raise PermissionDenied("User not found.")

        except jwt.ExpiredSignatureError:
            raise PermissionDenied("Access token has already expired.")
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid token:", str(e))
            raise PermissionDenied("Invalid access token.")

        return True



"""
this permission class should follow said procedures as below

1. super admin = these admins can do anything egs create,read,update,delete
2. admin = these admins can do anything except delete egs create,read,update
3. user = these users can only read and update and also they should only be able to see their own data


models 
1. Assets -- users cannot see assets
2. AssetRequests -- users can only see their own requests
3. AssetCheckouts -- users can only see their own checkouts
4. AssetReturns
5. Maintenance Reqests
6. Requestable assets -- users can see all requestable assets

"""
        
        

ROLE_SUPERADMIN = "superadmin"
ROLE_ADMIN = "admin"
ROLE_USER = "user"

class AdminCheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        
        role_permissions = {
            ROLE_SUPERADMIN: True,  # Full access
            ROLE_ADMIN: request.method != "DELETE",
            ROLE_USER: request.method in ["GET", "PUT", "PATCH"],
        }

        return role_permissions.get(getattr(request.user.role, "name", ""), False)

    def has_object_permission(self, request, view, obj):
        model = getattr(view, "queryset", view.get_queryset()).model
        role_name = getattr(request.user.role, "name", "")

        if role_name == ROLE_SUPERADMIN:
            return True
        
        if role_name == ROLE_ADMIN:
            return request.method != "DELETE"
        
        if role_name == ROLE_USER:
            allowed_methods = ["GET", "PUT", "PATCH"]
            if model.__name__ in ["AssetRequests", "AssetCheckOut", "AssetReturn", "AssetMaintenanceRequest"]:
                return getattr(obj, "user", None) == request.user and request.method in allowed_methods

            return getattr(obj, "owner", None) == request.user and request.method in allowed_methods
        
        return False



# class AdminCheckPermission(BasePermission):
#     def has_permission(self, request, view):
#         # Allow safe methods for all authenticated users
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return request.user.is_authenticated

#         # Define permission rules
#         if request.user.role.name == "superadmin":
#             return True  # Full access
        
#         if request.user.role.name == "admin":
#             # Allow everything except DELETE
#             return request.method != "DELETE"

#         if request.user.role.name == "user":
#             # Allow only read and update access
#             return request.method in ["GET", "PUT", "PATCH"]

#         return False

#     def has_object_permission(self, request, view, obj):
#         model = view.queryset.model if hasattr(view, 'queryset') else view.get_queryset().model

#         # Superadmin has access to all objects
#         if request.user.role.name == "superadmin":
#             return True

#         # Admin can access all objects except deleting them
#         if request.user.role.name == "admin":
#             return request.method != "DELETE"

#         # Regular users can only access their own data
#         if request.user.role.name == "user":
#             if model.__name__ in ["AssetRequests", "AssetCheckOut", "AssetReturn", "AssetMaintenanceRequest"]:
#                 return getattr(obj, 'user', None) == request.user and request.method in ["GET", "PUT", "PATCH"]

#             return obj.owner == request.user and request.method in ["GET", "PUT", "PATCH"]

#         return False
