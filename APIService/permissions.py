from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from APIService.models import UserDetails


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.username == request.user.username


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.owner == UserDetails.objects.get(user=request.user):
            return True
        return obj.owner == request.user
