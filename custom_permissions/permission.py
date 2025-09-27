# custom_permissions/permission.py
from rest_framework.permissions import BasePermission

class IsAdminOrAccountant(BasePermission):
    """
    Admin has full access.
    Accountant has all but delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Only admin can DELETE
        if request.method == "DELETE":
            return request.user.groups.filter(name="Admin").exists()

        return (
            request.user.groups.filter(name="Admin").exists() or
            request.user.groups.filter(name="Accountant").exists()
        )

from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminReadOnly(BasePermission):
    """
    Allow read-only access to admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
            and request.method in SAFE_METHODS
        )


class AuthenticatedReadOnly(BasePermission):
    """
    Allow authenticated users read-only access.
    """

    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.method in SAFE_METHODS
        )


class AccountantReadOnly(BasePermission):
    """
    Allow read-only access to accountant users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "accountant"
            and request.method in SAFE_METHODS
        )


class IsAdmin(BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )

class IsUser(BasePermission):
    """ just user"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "user"
        )
    
