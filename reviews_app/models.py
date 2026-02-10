from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Reviews(models.Model):
    business = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('5.0'))]
    )
    description = models.TextField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """A reviewer can only submit one review per business."""
        unique_together = [['business', 'reviewer']]

    def __str__(self):
        return f"Review {self.id} for business {self.business.user.username} by {self.reviewer.user.username}"
    