from django.db.models import Avg

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from offers_app.models import Offer
from reviews_app.models import Reviews
from profiles_app.models import Profile
from .serializers import BaseInfoSerializer


class BaseInfoView(APIView):
    """API view for retrieving platform statistics and base information."""

    permission_classes = [AllowAny]
    serializer_class = BaseInfoSerializer
    
    def get(self, request):
        review_count = Reviews.objects.count()
        
        avg_rating = Reviews.objects.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(float(avg_rating), 1) if avg_rating else 0.0
        
        business_profile_count = Profile.objects.filter(type='business').count()
        
        offer_count = Offer.objects.count()
        
        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
        
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
