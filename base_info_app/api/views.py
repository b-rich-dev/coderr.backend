from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Avg
from django.contrib.auth.models import User
from decimal import Decimal

from reviews_app.models import Reviews
from profiles_app.models import Profile
from offers_app.models import Offer
from .serializers import BaseInfoSerializer


class BaseInfoView(APIView):
    """API view for retrieving basic information about the application"""
    permission_classes = [AllowAny]
    serializer_class = BaseInfoSerializer
    
    def get(self, request):
        # Calculate statistics dynamically
        review_count = Reviews.objects.count()
        
        # Calculate average rating, rounded to one decimal place
        avg_rating = Reviews.objects.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(float(avg_rating), 1) if avg_rating else 0.0
        
        # Count business profiles
        business_profile_count = Profile.objects.filter(type='business').count()
        
        # Count offers
        offer_count = Offer.objects.count()
        
        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
        
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)