from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], default='customer')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        username = validated_data.pop('username')
        user_type = validated_data.pop('type', 'customer')

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
        )

        Token.objects.create(user=user)
        Profile.objects.create(user=user, type=user_type)
        
        return user
    