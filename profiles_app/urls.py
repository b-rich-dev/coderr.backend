from django.urls import path, include

urlpatterns = [
    path('', include('profiles_app.api.urls')),
]
