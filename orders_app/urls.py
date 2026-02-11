from django.urls import path, include


urlpatterns = [
    path('', include('orders_app.api.urls')),
]
