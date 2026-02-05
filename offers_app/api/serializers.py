from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.contrib.auth.models import User


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']


class OfferDetailListSerializer(serializers.ModelSerializer):
    """Serializer für OfferDetail in der GET Liste (nur id und url)"""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
    
    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class UserDetailsSerializer(serializers.Serializer):
    """Serializer für User-Details in der Angebotsliste"""
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer für GET Liste der Angebote"""
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
    
    def get_min_price(self, obj):
        """Berechnet den minimalen Preis aus den Details"""
        details = obj.offer_details.all()
        if details:
            return min(detail.price for detail in details)
        return None
    
    def get_min_delivery_time(self, obj):
        """Berechnet die minimale Lieferzeit aus den Details"""
        details = obj.offer_details.all()
        if details:
            return min(detail.delivery_time_in_days for detail in details)
        return None
    
    def get_user_details(self, obj):
        """Gibt User-Details zurück"""
        user = obj.creator.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer für POST zum Erstellen eines Angebots"""
    details = OfferDetailSerializer(source='offer_details', many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']
    
    def validate_offer_details(self, value):
        """Validiert, dass genau 3 Details vorhanden sind"""
        if len(value) != 3:
            raise serializers.ValidationError("Ein Angebot muss genau 3 Details enthalten.")
        return value
    
    def create(self, validated_data):
        """Erstellt ein Angebot mit den zugehörigen Details"""
        details_data = validated_data.pop('offer_details')
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    
    def to_representation(self, instance):
        """Verwendet OfferDetailSerializer für die Antwort"""
        representation = super().to_representation(instance)
        representation['details'] = OfferDetailSerializer(instance.offer_details.all(), many=True).data
        return representation
