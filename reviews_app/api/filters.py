import django_filters
from reviews_app.models import Reviews


class ReviewsFilter(django_filters.FilterSet):
    """Custom filter for Reviews to match API requirements."""
    
    business_user_id = django_filters.NumberFilter(field_name='business__user__id')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer__user__id')
    
    class Meta:
        model = Reviews
        fields = ['business_user_id', 'reviewer_id']
