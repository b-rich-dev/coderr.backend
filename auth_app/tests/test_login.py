from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class LoginTests(APITestCase):
        
    def setUp(self):
        """Erstellt einen Testbenutzer für die Login-Tests"""
        self.test_user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        
    def test_login_user(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['email'], "testuser@example.com")
        self.assertIn('user_id', response.data)

    def test_login_invalid_credentials(self):
        """Ungültige Anmeldeinformationen"""
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_login_missing_fields(self):
        """Fehlende Felder bei der Anmeldung"""
        url = reverse('login')
        data = {
            "username": "testuser"
            # Passwort fehlt
        }
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_login_nonexistent_user(self):
        """Anmeldung mit nicht existierendem Benutzer"""
        url = reverse('login')
        data = {
            "username": "nonexistent",
            "password": "somepassword"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_logout_user(self):
        """Testet die Abmeldung eines authentifizierten Benutzers"""
        # Zuerst anmelden, um ein Token zu erhalten
        login_url = reverse('login')
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data.get('token')
        
        # Prüfe dass Token existiert
        self.assertTrue(Token.objects.filter(key=token).exists())
        
        # Token zum Header hinzufügen
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Abmelde-URL aufrufen
        logout_url = reverse('logout')
        logout_response = self.client.post(logout_url, format='json')
        
        print(f"\n📩 Logout Response Status: {logout_response.status_code}")
        print(f"📦 Logout Response Data: {logout_response.data}\n")
        
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('message', logout_response.data)
        
        # Prüfe dass Token gelöscht wurde
        self.assertFalse(Token.objects.filter(key=token).exists())
        