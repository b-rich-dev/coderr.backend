from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile


class GetProfileDetailTests(APITestCase):
        
    def setUp(self):
        """Erstellt einen Testbenutzer und sein Profil für die Tests"""
        self.test_user = User.objects.create_user(username="profileuser", email="profileuser@example.com", password="testpassword")
        self.profile = Profile.objects.create(user=self.test_user, type="customer")
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_get_own_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "profileuser")
        self.assertEqual(response.data['email'], "profileuser@example.com")
        
    def test_get_other_user_profile(self):
        """Versucht, das Profil eines anderen Benutzers abzurufen"""
        other_user = User.objects.create_user(username="otheruser", email="otheruser@example.com", password="otherpassword")
        other_profile = Profile.objects.create(user=other_user, type="customer")
        url = reverse('profile-detail', args=[other_profile.id])
        response = self.client.get(url, format='json') 
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "otheruser")
        self.assertEqual(response.data['email'], "otheruser@example.com")

    def test_get_profile_unauthenticated(self):
        """Versucht, das Profil ohne Authentifizierung abzurufen"""
        self.client.credentials()  # Entfernt die Authentifizierungsinformationen
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_nonexistent_profile(self):
        """Versucht, ein nicht existentes Profil abzurufen"""
        url = reverse('profile-detail', args=[9999])  # Annahme: ID 9999 existiert nicht
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
