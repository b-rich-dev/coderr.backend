from django.urls import path, include


urlpatterns = [
    path('', include('reviews_app.api.urls')),
]
