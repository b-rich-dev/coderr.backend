from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile


class GetProfileDetailTests(APITestCase):
    """Testing the retrieval of profile information via the API"""
        
    def setUp(self):
        """Set up a test user and profile, and authenticate the client"""
        
        self.test_user = User.objects.create_user(username="profileuser", email="profileuser@example.com", password="testpassword")
        self.profile = Profile.objects.create(user=self.test_user, type="customer")
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_get_own_profile(self):
        """Retrieve the authenticated user's own profile"""
        
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "profileuser")
        self.assertEqual(response.data['email'], "profileuser@example.com")
        
    def test_get_other_user_profile(self):
        """Attempt to retrieve another user's profile"""
        
        other_user = User.objects.create_user(username="otheruser", email="otheruser@example.com", password="otherpassword")
        other_profile = Profile.objects.create(user=other_user, type="customer")
        url = reverse('profile-detail', args=[other_profile.id])
        response = self.client.get(url, format='json') 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "otheruser")
        self.assertEqual(response.data['email'], "otheruser@example.com")

    def test_get_profile_unauthenticated(self):
        """Attempt to retrieve a profile without authentication"""
        
        self.client.credentials()
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_nonexistent_profile(self):
        """Attempt to retrieve a nonexistent profile"""
        
        url = reverse('profile-detail', args=[9999])
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
