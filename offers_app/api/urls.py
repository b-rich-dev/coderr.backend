from django.urls import path
from .views import OffersListCreateView, OfferDetailView, OfferDetailItemView


urlpatterns = [
    path('offers/', OffersListCreateView.as_view(), name='offers-list-create'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailItemView.as_view(), name='offerdetail-detail'),
]
