from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile


class GetBusinessProfilesTests(APITestCase):
        
    def setUp(self):
        """Erstellt Testbenutzer und Profile für die Tests"""
        self.business_user = User.objects.create_user(username="businessuser", email="businessuser@example.com", password="password123")
        
    def test_get_business_profiles_authenticated(self):
        """Testet das Abrufen von Business-Profilen als authentifizierter Benutzer"""
        business_profile = Profile.objects.create(
            user=self.business_user,
            type="business",
            location="Business City",
            tel="1234567890",
            description="A business profile",
            working_hours="9-5"
        )
        
        token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('businessprofiles')
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], "businessuser")
        self.assertEqual(response.data[0]['type'], "business")
        
        # Stelle sicher, dass email und created_at NICHT in der Antwort sind
        self.assertNotIn('email', response.data[0])
        self.assertNotIn('created_at', response.data[0])
        
    def test_get_business_profiles_unauthenticated(self):
        """Testet das Abrufen von Business-Profilen ohne Authentifizierung"""
        url = reverse('businessprofiles')
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        