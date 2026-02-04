from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_app.models import UserProfile
from auth_app.api.serializers import RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationTests(APITestCase):
        
    def test_register_user(self):
        url = reverse('registration')
        data = {
            "username": "John_Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], "John_Doe")
        self.assertEqual(response.data['email'], "john.doe@example.com")
        self.assertIn('user_id', response.data)
        