from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'You can only update your own posts.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
