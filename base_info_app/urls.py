from django.urls import path, include

urlpatterns = [
    path('', include('base_info_app.api.urls')),
]
