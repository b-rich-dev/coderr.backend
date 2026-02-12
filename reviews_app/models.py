from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Reviews(models.Model):
    """Model representing a review submitted by a reviewer for a business profile."""
    
    business = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """A reviewer can only submit one review per business."""
        
        unique_together = [['business', 'reviewer']]

    def __str__(self):
        return f"Review {self.id} for business {self.business.user.username} by {self.reviewer.user.username}"
    