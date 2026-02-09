from rest_framework import serializers
from rest_framework.exceptions import NotFound
from orders_app.models import Orders
from offers_app.models import OfferDetail


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for listing orders"""
    customer_user = serializers.IntegerField(source='customer.user.id', read_only=True)
    business_user = serializers.IntegerField(source='business.user.id', read_only=True)
    
    class Meta:
        model = Orders
        fields = [
            'id', 
            'customer_user',
            'business_user',
            'title', 
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'customer_user', 'business_user', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders with snapshot from OfferDetail"""
    offer_detail_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Orders
        fields = ['offer_detail_id']
    
    def validate_offer_detail_id(self, value):
        """Validate that the offer detail exists"""
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise NotFound("The specified offer details could not be found.")
        return value
    
    def create(self, validated_data):
        """Create order with snapshot of offer detail data"""
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.select_related('offer__creator').get(id=offer_detail_id)
        
        # Create order with snapshot data
        order = Orders.objects.create(
            offer_detail=offer_detail,
            customer=self.context['request'].user.profile,
            business=offer_detail.offer.creator,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type
        )
        return order
    
    def to_representation(self, instance):
        """Return full order data after creation without updated_at"""
        data = OrderListSerializer(instance).data
        data.pop('updated_at', None)
        return data
    

class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status"""
    
    class Meta:
        model = Orders
        fields = ['status']
    
    def to_representation(self, instance):
        """Return full order data after update"""
        return OrderListSerializer(instance).data
    