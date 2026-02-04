from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_app.models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], default='customer')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password', 'type']
    
    # def to_representation(self, instance):
    #     """
    #     Combines first_name and last_name into fullname for the response.
    #     Args:
    #         instance: The User model instance          
    #     Returns:
    #         dict: Serialized data with fullname instead of separate name fields
    #     """
    #     data = super().to_representation(instance)
    #     data['username'] = f"{instance.first_name} {instance.last_name}".strip()
    #     return data

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
        # name_parts = username.split(' ', 1)
        # first_name = name_parts[0] if len(name_parts) > 0 else ''
        # last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            # first_name=first_name,
            # last_name=last_name
        )

        Token.objects.create(user=user)
        UserProfile.objects.create(user=user, type=user_type)
        
        return user
    