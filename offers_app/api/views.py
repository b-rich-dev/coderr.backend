from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from offers_app.models import Offer, OfferDetail
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferDetailViewSerializer, OfferDetailViewUpdateSerializer, OfferDetailSerializer
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly
from .filters import OfferFilter


class OfferPagination(PageNumberPagination):
    """Pagination for offers"""
    page_size = 6
    page_size_query_param = 'page_size'
    #max_page_size = 100


class OffersListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().prefetch_related('offer_details', 'creator__user')
    permission_classes = [IsBusinessUser]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer
    
    def perform_create(self, serializer):
        """Set the current user's profile as creator"""
        serializer.save(creator=self.request.user.profile)
    
    def create(self, request, *args, **kwargs):
        """Override create to return custom status code 201"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().prefetch_related('offer_details', 'creator__user')
    serializer_class = OfferDetailViewSerializer
    permission_classes = [IsOfferOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferDetailViewUpdateSerializer
        return OfferDetailViewSerializer
    
    
class OfferDetailItemView(generics.RetrieveAPIView):
    """API view for retrieving a single OfferDetail"""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]    
