from rest_framework.permissions import BasePermission, SAFE_METHODS

from utils.choices import ClientGroupChoices


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (
                request.user.is_authenticated and
                request.user.is_admin
            )
        )


class ReadPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated or (request.user.is_authenticated and request.user.client_group == ClientGroupChoices.PARTIAL):
            return False
        return True


class ReadBcOrPrPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action != "retrieve":
            if not request.user.is_authenticated or (request.user.is_authenticated and request.user.client_group == ClientGroupChoices.PARTIAL):
                return False
        return True


class IsSuperUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False
