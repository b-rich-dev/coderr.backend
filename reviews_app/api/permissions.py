from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    """
    Permission to only allow customer users (not business users) to create reviews.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if request.user and request.user.is_authenticated:
            return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'
        
        return False
    

class IsReviewerOrReadOnly(BasePermission):
    """
    Custom permission to only allow the reviewer of a review to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.reviewer.user == request.user
