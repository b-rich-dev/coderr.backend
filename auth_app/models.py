from django.db import models

# UserProfile nicht mehr benötigt - Profile liegt jetzt in profiles_app
# class UserProfile(models.Model):
#     TYPE_CHOICES = [("customer", "Customer"), ("business", "Business"),]
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='userprofile')
#     type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="customer")

#     def __str__(self):
#         return f"{self.user.username} ({self.type})"
