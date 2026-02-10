from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.models import User

from reviews_app.models import Reviews
from profiles_app.models import Profile
from .serializers import ReviewsListSerializer
from .permissions import IsCustomerUser, IsReviewerOrReadOnly


class ReviewsListCreateView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all().order_by('-rating', '-created_at')
    serializer_class = ReviewsListSerializer
    
    def get_permissions(self):
        """Only customer users can create reviews, but any authenticated user can read"""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """The logged-in user is automatically the reviewer"""
        reviewer_profile = Profile.objects.get(user=self.request.user)
        serializer.save(reviewer=reviewer_profile)
    

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsListSerializer
    permission_classes = [IsAuthenticated, IsReviewerOrReadOnly]
    
    def get_permissions(self):
        """Only the reviewer can update or delete their review, but any authenticated user can read"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsReviewerOrReadOnly()]
        return [IsAuthenticated()]