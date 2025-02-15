from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):

        return request.method in SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
