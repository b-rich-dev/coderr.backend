from django.db.models import Q, Min
from django_filters import rest_framework as filters

from offers_app.models import Offer


class OfferFilter(filters.FilterSet):
    """Filter class for Offer model"""
    
    creator_id = filters.NumberFilter(field_name='creator__user__id')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time', 'search']
    
    def filter_min_price(self, queryset, name, value):
        """Filter by minimum price calculated from offer details"""
        
        return queryset.annotate(
            calculated_min_price=Min('offer_details__price')
        ).filter(calculated_min_price__gte=value)
    
    def filter_max_delivery_time(self, queryset, name, value):
        """Filter by maximum delivery time calculated from offer details"""
        
        return queryset.annotate(
            calculated_min_delivery=Min('offer_details__delivery_time_in_days')
        ).filter(calculated_min_delivery__lte=value)
    
    def filter_search(self, queryset, name, value):
        """Search in title and description"""
        
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
