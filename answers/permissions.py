from rest_framework import permissions


class AnswerOwnerOrAdmPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id or request.user.is_superuser