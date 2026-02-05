from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Berechtigung, die nur Business-Usern das Erstellen von Angeboten erlaubt.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        return hasattr(request.user, 'profile') and request.user.profile.type == 'business'
