from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from reviews_app.models import Reviews
from offers_app.models import Offer


class BaseInfoTests(APITestCase):
    
    def setUp(self):
        """Create test data"""
        # Create customer users
        self.customer1 = User.objects.create_user(username="customer1", password="pass123")
        self.customer_profile1 = Profile.objects.create(user=self.customer1, type='customer')
        
        self.customer2 = User.objects.create_user(username="customer2", password="pass123")
        self.customer_profile2 = Profile.objects.create(user=self.customer2, type='customer')
        
        # Create business users
        self.business1 = User.objects.create_user(username="business1", password="pass123")
        self.business_profile1 = Profile.objects.create(user=self.business1, type='business')
        
        self.business2 = User.objects.create_user(username="business2", password="pass123")
        self.business_profile2 = Profile.objects.create(user=self.business2, type='business')
        
        self.business3 = User.objects.create_user(username="business3", password="pass123")
        self.business_profile3 = Profile.objects.create(user=self.business3, type='business')
        
        # Create offers
        Offer.objects.create(
            creator=self.business_profile1,
            title="Web Development",
            description="Professional web development services"
        )
        Offer.objects.create(
            creator=self.business_profile2,
            title="Logo Design",
            description="Creative logo design"
        )
        
        # Create reviews
        Reviews.objects.create(business=self.business_profile1, reviewer=self.customer_profile1, rating=5, description="Excellent!")
        Reviews.objects.create(business=self.business_profile2, reviewer=self.customer_profile1, rating=4, description="Good!")
        Reviews.objects.create(business=self.business_profile3, reviewer=self.customer_profile2, rating=4.5, description="Very good!")
    
    def test_get_base_info(self):
        """Test retrieving base info statistics"""
        url = reverse('base-info')
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('review_count', response.data)
        self.assertIn('average_rating', response.data)
        self.assertIn('business_profile_count', response.data)
        self.assertIn('offer_count', response.data)
        
        # Check actual values
        self.assertEqual(response.data['review_count'], 3)
        self.assertEqual(response.data['average_rating'], 4.5)  # (5 + 4 + 4.5) / 3 = 4.5
        self.assertEqual(response.data['business_profile_count'], 3)
        self.assertEqual(response.data['offer_count'], 2)
    
    def test_get_base_info_no_authentication_required(self):
        """Test that base info can be retrieved without authentication"""
        url = reverse('base-info')
        # No credentials set
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_base_info_empty_database(self):
        """Test retrieving base info with no data"""
        # Delete all test data
        Reviews.objects.all().delete()
        Offer.objects.all().delete()
        Profile.objects.filter(type='business').delete()
        
        url = reverse('base-info')
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['review_count'], 0)
        self.assertEqual(response.data['average_rating'], 0.0)
        self.assertEqual(response.data['business_profile_count'], 0)
        self.assertEqual(response.data['offer_count'], 0)
