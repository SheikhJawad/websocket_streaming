from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Allows access only to superadmins (is_superuser=True).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsAdmin(BasePermission):
    """
    Allows access only to admins (is_staff=True, is_superuser=False).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and not request.user.is_superuser

