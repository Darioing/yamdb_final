from rest_framework import permissions

from authentication.models import ADMIN, MODERATOR


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or (request.auth and request.user.role == ADMIN)
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in [ADMIN, MODERATOR]
        )
