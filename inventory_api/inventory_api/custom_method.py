import re
from inventory_api.utils import decodeJWT
from rest_framework.permissions import BasePermission


class IsAuthenticatedCustom(BasePermission):
    """
    Here we are creating our own custom permission so if user does not have a access
    token user is not allowed to access the API

    """

    def has_permission(self, request, _):
        try:
            auth_token = request.META.get("HTTP_AUTHORIZATION", None)
        except Exception:
            return False
        if not auth_token:
            return False
        user = decodeJWT(auth_token)

        if not user:
            return False
        request.user = user
        return True
