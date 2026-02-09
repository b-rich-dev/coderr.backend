from django.db import models

class Orders(models.Model):
    offer_detail = models.ForeignKey('offers_app.OfferDetail', on_delete=models.PROTECT, related_name='orders')
    customer = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='customer_orders')
    business = models.ForeignKey('profiles_app.Profile', on_delete=models.CASCADE, related_name='business_orders')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='in_progress')

    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], default='standard')
    

    def __str__(self):
        return f"Order {self.id} for {self.title} by {self.customer.user.username}"
    