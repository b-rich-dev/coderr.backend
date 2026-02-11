from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Reviews
from profiles_app.models import Profile
from .serializers import ReviewsListSerializer
from .permissions import IsCustomerUser, IsReviewerOrReadOnly


class ReviewsListCreateView(generics.ListCreateAPIView):
    """View to list all reviews and allow customer users to create new reviews."""
    
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
    """View to retrieve, update, or delete a specific review."""
    
    queryset = Reviews.objects.all()
    serializer_class = ReviewsListSerializer
    permission_classes = [IsAuthenticated, IsReviewerOrReadOnly]
    
    def get_permissions(self):
        """Only the reviewer can update or delete their review, but any authenticated user can read"""
        
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsReviewerOrReadOnly()]
        return [IsAuthenticated()]
