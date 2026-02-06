from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Min

from offers_app.models import Offer, OfferDetail
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferDetailViewSerializer, OfferDetailViewUpdateSerializer, OfferDetailSerializer
from .permissions import IsBusinessUser, IsOfferOwnerOrReadOnly


class OfferPagination(PageNumberPagination):
    """Pagination for offers"""
    page_size = 6
    page_size_query_param = 'page_size'
    #max_page_size = 100


class OffersListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessUser]
    pagination_class = OfferPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer
    
    def get_queryset(self):
        """Filter and sort offers based on query parameters"""
        queryset = Offer.objects.all().prefetch_related('offer_details', 'creator__user')
        
        # Filter by creator_id
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id:
            queryset = queryset.filter(creator__user__id=creator_id)
        
        # Filter by min_price (calculated from details)
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.annotate(
                calculated_min_price=Min('offer_details__price')
            ).filter(calculated_min_price__gte=min_price)
        
        # Filter by max_delivery_time (calculated from details)
        max_delivery_time = self.request.query_params.get('max_delivery_time', None)
        if max_delivery_time:
            queryset = queryset.annotate(
                calculated_min_delivery=Min('offer_details__delivery_time_in_days')
            ).filter(calculated_min_delivery__lte=max_delivery_time)
        
        # Search in title and description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        # Ordering
        ordering = self.request.query_params.get('ordering', None)
        if ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')
        elif ordering == '-updated_at':
            queryset = queryset.order_by('-updated_at')
        elif ordering == 'min_price':
            queryset = queryset.annotate(
                calculated_min_price=Min('offer_details__price')
            ).order_by('calculated_min_price')
        elif ordering == '-min_price':
            queryset = queryset.annotate(
                calculated_min_price=Min('offer_details__price')
            ).order_by('-calculated_min_price')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
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
