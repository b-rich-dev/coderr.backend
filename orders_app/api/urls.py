from django.urls import path
from .views import OrdersListCreateView, OrderDetailView, OrderCountView


urlpatterns = [
    path('orders/', OrdersListCreateView.as_view(), name='orders-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
]
