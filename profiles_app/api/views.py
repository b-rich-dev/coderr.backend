from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from profiles_app.models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from .permissions import IsOwnerOrReadOnly
    

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        response_serializer = ProfileSerializer(instance)
        return Response(response_serializer.data) 
    
    
class BusinessView(APIView):
    """API view für alle Business Profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        business_profiles = Profile.objects.filter(type='business')
        serializer = ProfileSerializer(business_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CustomerView(APIView):
    """API view für alle Customer Profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        customer_profiles = Profile.objects.filter(type='customer')
        serializer = ProfileSerializer(customer_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)