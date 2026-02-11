from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegistrationTests(APITestCase):
    """Test suite for user registration endpoint."""
        
    def test_register_user(self):
        """Tests successful user registration with valid data."""
        
        url = reverse('registration')
        data = {
            "username": "John_Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], "John_Doe")
        self.assertEqual(response.data['email'], "john.doe@example.com")
        self.assertIn('user_id', response.data)
    
    def test_register_duplicate_email(self):
        """Tests registration attempt with duplicate email address."""
        
        url = reverse('registration')

        User.objects.create_user(username='existing', email='test@test.com', password='pass123')
        
        data = {
            "username": "NewUser",
            "email": "test@test.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_register_password_mismatch(self):
        """Tests registration with mismatched passwords."""
        
        url = reverse('registration')
        data = {
            "username": "TestUser",
            "email": "test@test.com",
            "password": "pass123",
            "repeated_password": "different",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_missing_fields(self):
        """Tests registration with missing required fields."""
        
        url = reverse('registration')
        data = {"email": "test@test.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_invalid_type(self):
        """Tests registration with invalid user type."""
        
        url = reverse('registration')
        data = {
            "username": "TestUser",
            "email": "test@test.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "invalid"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_profile_created_customer(self):
        """Tests that a profile with type 'customer' is created."""
        
        url = reverse('registration')
        data = {
            "username": "CustomerUser",
            "email": "customer@test.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email="customer@test.com")
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.type, 'customer')
    
    def test_profile_created_business(self):
        """Tests that a profile with type 'business' is created."""
        
        url = reverse('registration')
        data = {
            "username": "BusinessUser",
            "email": "business@test.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "business"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email="business@test.com")
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.type, 'business')
    
    def test_token_created_on_registration(self):
        """Tests that an authentication token is automatically created."""
        
        url = reverse('registration')
        data = {
            "username": "TokenUser",
            "email": "token@test.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email="token@test.com")
        self.assertTrue(Token.objects.filter(user=user).exists())
 