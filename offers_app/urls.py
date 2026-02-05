from django.urls import path, include

urlpatterns = [
    path('', include('offers_app.api.urls')),
]
