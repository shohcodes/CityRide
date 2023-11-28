from rest_framework.permissions import BasePermission


class DriverOrderPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return bool(request.user and request.user.is_authenticated)
