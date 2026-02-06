from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.contrib.auth.models import User


class OfferPriceDeliveryMixin:
    """Mixin for calculating min_price and min_delivery_time from offer details"""
    
    def get_min_price(self, obj):
        """Calculate the minimum price from offer details"""
        details = obj.offer_details.all()
        if details:
            return min(detail.price for detail in details)
        return None
    
    def get_min_delivery_time(self, obj):
        """Calculate the minimum delivery time from offer details"""
        details = obj.offer_details.all()
        if details:
            return min(detail.delivery_time_in_days for detail in details)
        return None
    
        
class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']


class OfferDetailListSerializer(serializers.ModelSerializer):
    """Serializer for OfferDetail in GET list (id and url only)"""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = ['id', 'url']
    
    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailViewSerializer(OfferPriceDeliveryMixin, serializers.ModelSerializer):
    user = serializers.IntegerField(source='creator.user.id', read_only=True)
    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        read_only_fields = ['id']
        
        
        
class OfferDetailViewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for PATCH/PUT operations on offers with nested detail updates"""
    details = OfferDetailSerializer(source='offer_details', many=True, required=False)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        """Update offer and its associated details"""
        details_data = validated_data.pop('offer_details', None)
        
        # Update offer fields dynamically
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        
        # Update details if provided
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    # Find and update detail by offer_type
                    try:
                        detail = OfferDetail.objects.get(offer=instance, offer_type=offer_type)
                        for field, value in detail_data.items():
                            setattr(detail, field, value)
                        detail.save()
                    except OfferDetail.DoesNotExist:
                        pass
        
        return instance
    
    def to_representation(self, instance):
        """Use full OfferDetailSerializer for response"""
        representation = {
            'id': instance.id,
            'title': instance.title,
            'image': instance.image.url if instance.image else None,
            'description': instance.description,
            'details': OfferDetailSerializer(instance.offer_details.all(), many=True).data
        }
        return representation


class UserDetailsSerializer(serializers.Serializer):
    """Serializer for user details in offer list"""
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(OfferPriceDeliveryMixin, serializers.ModelSerializer):
    """Serializer for GET list of offers"""
    user = serializers.IntegerField(source='creator.user.id', read_only=True)
    details = OfferDetailListSerializer(source='offer_details', many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = [
            'id', 
            'user',
            'title', 
            'image', 
            'description',
            'created_at', 
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_details(self, obj):
        """Return user details for the offer creator"""
        user = obj.creator.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for POST to create a new offer"""
    details = OfferDetailSerializer(source='offer_details', many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']
    
    def validate_details(self, value):
        """Validate that exactly 3 details are provided"""
        if len(value) != 3:
            raise serializers.ValidationError("An offer must contain exactly 3 details.")
        return value
    
    def create(self, validated_data):
        """Create an offer with associated details"""
        details_data = validated_data.pop('offer_details')
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    
    def to_representation(self, instance):
        """Use OfferDetailSerializer for response representation"""
        representation = super().to_representation(instance)
        representation['details'] = OfferDetailSerializer(instance.offer_details.all(), many=True).data
        return representation
