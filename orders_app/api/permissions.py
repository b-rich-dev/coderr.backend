from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Permission: Only users with type 'customer' can create orders, but all authenticated users can view"""
    
    def has_permission(self, request, view):
        # Only customers can create orders
        if request.method == 'POST':
            return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'
        # All authenticated users (customer and business) can view orders
        return True


class IsOrderParticipant(permissions.BasePermission):
    """Permission: Only customer or business of the order can access it"""
    
    def has_object_permission(self, request, view, obj):
        # Only staff/admin can delete orders
        if request.method == 'DELETE':
            return request.user.is_staff
        
        # Check if user has profile (staff users may not have one)
        if not hasattr(request.user, 'profile'):
            return False
            
        user_profile = request.user.profile
        
        # Business can update
        if request.method in ['PUT', 'PATCH']:
            return obj.business == user_profile
        
        # GET: both customer and business can access
        return obj.customer == user_profile or obj.business == user_profile
