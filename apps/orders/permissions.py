from rest_framework.permissions import BasePermission


class DriverOrderPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.role == 'driver'
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return obj.driver == request.user
        return request.user.is_authenticated


class ClientOrderPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.role == 'client'
        return request.user.is_authenticated
