from rest_framework import permissions


class UsersListManageAuthentication(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated or request.method == "POST":
            return True

        return False


class UserProfileManageAuthentication(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj or request.user.is_superuser or request.method in permissions.SAFE_METHODS:
            return True
        return False
