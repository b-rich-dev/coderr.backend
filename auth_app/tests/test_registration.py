from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
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
    
    def test_register_duplicate_email(self):
        """Email bereits registriert"""
        url = reverse('registration')
        # Ersten User erstellen
        User.objects.create_user(username='existing', email='test@test.com', password='pass123')
        
        # Zweiten mit gleicher Email versuchen
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
        """Passwörter stimmen nicht überein"""
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
        """Pflichtfelder fehlen"""
        url = reverse('registration')
        data = {"email": "test@test.com"}  # username und password fehlen
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_invalid_type(self):
        """Ungültiger User Type"""
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
        """Prüft ob Profile mit Type 'customer' erstellt wurde"""
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
        """Prüft ob Profile mit Type 'business' erstellt wurde"""
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
        """Prüft ob Token automatisch erstellt wird"""
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
 