from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class LoginTests(APITestCase):
    """Test suite for authentication endpoints (login and logout)."""
        
    def setUp(self):
        """Creates a test user for login tests."""
        
        self.test_user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        
    def test_login_user(self):
        """Tests successful user login with valid credentials."""
        
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['email'], "testuser@example.com")
        self.assertIn('user_id', response.data)

    def test_login_invalid_credentials(self):
        """Tests login attempt with invalid password."""
        
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_login_missing_fields(self):
        """Tests login attempt with missing required fields."""
        
        url = reverse('login')
        data = {
            "username": "testuser"
            # Password is missing
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_login_nonexistent_user(self):
        """Tests login attempt with non-existent username."""
        
        url = reverse('login')
        data = {
            "username": "nonexistent",
            "password": "somepassword"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_logout_user(self):
        """Tests user logout functionality."""
        
        login_url = reverse('login')
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token')
        
        self.assertTrue(Token.objects.filter(key=token).exists())
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        logout_url = reverse('logout')
        logout_response = self.client.post(logout_url, format='json')
        
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('message', logout_response.data)
        
        self.assertFalse(Token.objects.filter(key=token).exists())
        