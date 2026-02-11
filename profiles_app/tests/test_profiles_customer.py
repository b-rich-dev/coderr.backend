from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile


class GetCustomerProfilesTests(APITestCase):
        
    def setUp(self):
        """Creates test users and profiles for the tests"""
        
        self.customer_user = User.objects.create_user(
            username="customeruser", 
            email="customeruser@example.com", 
            password="password123"
        )
        
    def test_get_customer_profiles_authenticated(self):
        """Tests retrieving customer profiles as an authenticated user"""
        
        customer_profile = Profile.objects.create(
            user=self.customer_user,
            type="customer",
            location="Customer City",
            tel="0987654321",
            description="A customer profile",
            working_hours="10-6"
        )
        
        token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('customerprofiles')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], "customeruser")
        self.assertEqual(response.data[0]['type'], "customer")
        
    def test_get_customer_profiles_unauthenticated(self):
        """Tests retrieving customer profiles without authentication"""
        
        url = reverse('customerprofiles')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
      