from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Profile model extending the User model with additional fields"""
    
    TYPE_CHOICES = [("customer", "Customer"), ("business", "Business"),]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="customer")
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"
