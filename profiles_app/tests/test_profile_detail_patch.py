from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile


class PatchProfileTests(APITestCase):
    
    def setUp(self):
        """Erstellt Testbenutzer und Profile für PATCH-Tests"""
        self.test_user = User.objects.create_user(username="patchuser", email="patch@example.com", password="testpass")
        self.profile = Profile.objects.create(user=self.test_user, type="customer")
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_patch_own_profile_full(self):
        """Patcht eigenes Profil mit allen Feldern"""
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "location": "Berlin",
            "tel": "123456789",
            "description": "Software Developer",
            "working_hours": "9-17",
            "email": "john.doe@example.com"
        }
        response = self.client.patch(url, data, format='json')
        
        print(f"\n📩 PATCH Response Status: {response.status_code}")
        print(f"📦 PATCH Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")
        self.assertEqual(response.data['last_name'], "Doe")
        self.assertEqual(response.data['location'], "Berlin")
        self.assertEqual(response.data['tel'], "123456789")
        self.assertEqual(response.data['description'], "Software Developer")
        self.assertEqual(response.data['working_hours'], "9-17")
        self.assertEqual(response.data['email'], "john.doe@example.com")
        
        # Prüfe dass User-Felder auch im User-Model aktualisiert wurden
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.first_name, "John")
        self.assertEqual(self.test_user.last_name, "Doe")
        self.assertEqual(self.test_user.email, "john.doe@example.com")
    
    def test_patch_own_profile_partial(self):
        """Patcht nur einzelne Felder des eigenen Profils"""
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            "location": "München"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], "München")
        # Andere Felder bleiben unverändert
        self.assertEqual(response.data['username'], "patchuser")
    
    def test_patch_other_user_profile(self):
        """Versucht, fremdes Profil zu patchen - sollte verboten sein"""
        other_user = User.objects.create_user(username="otheruser", email="other@example.com", password="otherpass")
        other_profile = Profile.objects.create(user=other_user, type="customer")
        
        url = reverse('profile-detail', args=[other_profile.id])
        data = {"location": "Hamburg"}
        response = self.client.patch(url, data, format='json')
        
        print(f"\n📩 PATCH Other User Response Status: {response.status_code}")
        print(f"📦 PATCH Other User Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_patch_profile_unauthenticated(self):
        """Versucht, Profil ohne Authentifizierung zu patchen"""
        self.client.credentials()  # Entfernt Token
        url = reverse('profile-detail', args=[self.profile.id])
        data = {"location": "Frankfurt"}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_patch_profile_read_only_fields(self):
        """Versucht, read-only Felder zu ändern - sollten ignoriert werden"""
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            "type": "business",  # read-only
            "username": "newusername",  # read-only
            "location": "Köln"  # erlaubt
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], "Köln")  # wurde geändert
        self.assertEqual(response.data['type'], "customer")  # blieb customer
        self.assertEqual(response.data['username'], "patchuser")  # blieb gleich
        