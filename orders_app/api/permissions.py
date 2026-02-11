from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Permission: Only users with type 'customer' can create orders, but all authenticated users can view"""
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'
        return True


class IsOrderParticipant(permissions.BasePermission):
    """Permission: Only customer or business of the order can access it"""
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff
        
        if not hasattr(request.user, 'profile'):
            return False
            
        user_profile = request.user.profile
        
        if request.method in ['PUT', 'PATCH']:
            return obj.business == user_profile
        
        return obj.customer == user_profile or obj.business == user_profile
