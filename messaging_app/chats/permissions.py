from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        # Read permissions are allowed to any authenticated request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Write permissions are only allowed to the owner
        return obj.owner == request.user