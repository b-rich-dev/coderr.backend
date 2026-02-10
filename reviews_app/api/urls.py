from django.urls import path
from .views import ReviewsListCreateView, ReviewDetailView


urlpatterns = [
    path('reviews/', ReviewsListCreateView.as_view(), name='reviews-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
