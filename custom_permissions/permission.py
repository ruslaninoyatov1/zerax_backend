# custom_permissions/permission.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminOrAccountant(BasePermission):
    """
    Admin has full access.
    Accountant has all but delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == "DELETE":
            return request.user.role == "admin"
        return request.user.role in ["admin", "accountant"]

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
        return (
            request.user and request.user.is_authenticated and
            getattr(request.user, 'role',None) == 'admin'
        )


class IsUser(BasePermission):
    """ just user"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "user"
        )

# New
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, "role", None) in ("admin", "accountant"):
            return True

        return getattr(obj, "user", None) == request.user

class IsAccountant(permissions.BasePermission):
    """Accountant – hamma narsani ko‘rish va tahrir qilish mumkin, lekin o‘chira olmaydi."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "accountant":
            return False
        if request.method == "DELETE":
            return False
        return True

class IsOwnerOrAdminOrAccountant(permissions.BasePermission):
    """
    Admin va accountant – hamma narsaga ruxsat.
    Oddiy user – faqat o‘z invoice’ini CRUD qilishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin','accountant']:
            return True
        return obj.user == request.user

