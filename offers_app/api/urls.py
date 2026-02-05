from django.urls import path
from .views import OffersListCreateView


urlpatterns = [
    path('offers/', OffersListCreateView.as_view(), name='offers-list-create'),
    #path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    
    # path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    # path('upload/', ProfileDetailView.as_view(), name='profile-upload'),
    # path('profiles/business/', BusinessView.as_view(), name='businessprofiles'),
    # path('profiles/customer/', CustomerView.as_view(), name='customerprofiles'),
]
