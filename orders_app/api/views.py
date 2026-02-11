from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from orders_app.models import Orders
from .permissions import IsOrderParticipant, IsCustomerUser
from .serializers import OrderListSerializer, OrderCreateSerializer, OrderUpdateSerializer


class OrdersListCreateView(generics.ListCreateAPIView):
    """API view for listing and creating orders"""
    
    queryset = Orders.objects.all()
    permission_classes = [IsAuthenticated, IsCustomerUser]
    
    def get_queryset(self):
        """Return orders where user is either customer or business"""
        
        user_profile = self.request.user.profile
        return Orders.objects.filter(
            Q(customer=user_profile) | Q(business=user_profile)
        ).select_related('customer__user', 'business__user')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, or deleting a single order"""
    
    queryset = Orders.objects.all().select_related('customer__user', 'business__user')
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, IsOrderParticipant]
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OrderUpdateSerializer
        return OrderListSerializer


class OrderCountView(APIView):
    """API view for getting the count of in-progress orders for a business user"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, business_user_id):
        """Get count of in-progress orders for a business user"""

        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            raise NotFound("No business user matching the specified ID was found.")
        
        order_count = Orders.objects.filter(business__user__id=business_user_id, status='in_progress').count()
        
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)
 

class CompletedOrderCountView(APIView):
    """API view for getting the count of completed orders for a business user"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, business_user_id):
        """Get count of completed orders for a business user"""
        
        try:
            business_user = User.objects.get(id=business_user_id)
        except User.DoesNotExist:
            raise NotFound("No business user matching the specified ID was found.")
        
        order_count = Orders.objects.filter(business__user__id=business_user_id, status='completed').count()
        
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)
    