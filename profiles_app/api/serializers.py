from django.contrib.auth.models import User

from rest_framework import serializers

from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        ]
        read_only_fields = ['user', 'username', 'email', 'type', 'created_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'email',
        ]
    
    def update(self, instance, validated_data):
        
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        
        if first_name is not None:
            instance.user.first_name = first_name
        if last_name is not None:
            instance.user.last_name = last_name
        if email is not None:
            instance.user.email = email
        
        if first_name or last_name or email:
            instance.user.save()
        
        # Update Profile Felder
        return super().update(instance, validated_data)