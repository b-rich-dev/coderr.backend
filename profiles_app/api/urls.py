from django.urls import path
from .views import ProfileDetailView, BusinessView, CustomerView


urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('upload/', ProfileDetailView.as_view(), name='profile-upload'),
    path('profiles/business/', BusinessView.as_view(), name='businessprofiles'),
    path('profiles/customer/', CustomerView.as_view(), name='customerprofiles'),
]