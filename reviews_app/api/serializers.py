from django.contrib.auth.models import User

from rest_framework import serializers

from reviews_app.models import Reviews
from profiles_app.models import Profile


class ReviewsListSerializer(serializers.ModelSerializer):
    """Serializer for Reviews model with custom validation to prevent duplicate reviews."""
    
    business_user = serializers.SerializerMethodField()
    reviewer = serializers.IntegerField(source='reviewer.user.id', read_only=True)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    
    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']
    
    def get_business_user(self, obj):
        return obj.business.user.id
    
    def to_internal_value(self, data):
        self._business_profile_id = None
        if 'business_user' in data:
            business_user_id = data['business_user']
            try:
                user = User.objects.get(id=business_user_id)
                profile = Profile.objects.get(user=user)
                self._business_profile_id = profile.id
            except (User.DoesNotExist, Profile.DoesNotExist):
                raise serializers.ValidationError({"business_user": "Business user not found."})
        
        data_copy = data.copy()
        data_copy.pop('business_user', None)
        return super().to_internal_value(data_copy)
    
    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(self, '_business_profile_id'):
            reviewer_profile = Profile.objects.get(user=request.user)
            if Reviews.objects.filter(business_id=self._business_profile_id, reviewer=reviewer_profile).exists():
                raise serializers.ValidationError("You have already submitted a review for this business user.")
        return data
    
    def create(self, validated_data):
        if hasattr(self, '_business_profile_id') and self._business_profile_id:
            validated_data['business_id'] = self._business_profile_id
        return super().create(validated_data)
        