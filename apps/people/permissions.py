from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
import jwt
import arrow
from decouple import config
import logging

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


class AdminCheckPermission(BasePermission):
    def has_permission(self, request, view):
        admins = ["admin", "superuser", "manager"]
        if request.user.role.name in admins:
            return True
        else:
            raise PermissionDenied("Only admins can perform this action.")
