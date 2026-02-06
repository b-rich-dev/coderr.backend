from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Permission that only allows business users to create offers.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        return hasattr(request.user, 'profile') and request.user.profile.type == 'business'


class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission that allows only the offer owner to update or delete it.
    Read-only access is allowed for authenticated users.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.creator.user == request.user
