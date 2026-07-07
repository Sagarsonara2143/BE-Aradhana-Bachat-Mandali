from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.accounts.models import UserRole


class IsAdminRole(BasePermission):
    """Allow only admin-role users (Super Admin / Website Admin / Content Manager)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin_role)


class IsMember(BasePermission):
    """Allow only member-role (or admin) users."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return user.role == UserRole.MEMBER or user.is_admin_role


class ReadOnlyOrAdmin(BasePermission):
    """Public read access; writes require an admin role."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin_role)
