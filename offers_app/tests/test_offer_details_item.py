from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail


class GetOfferDetailTests(APITestCase):
    """Test suite for retrieving offer details"""
    
    def setUp(self):
        """Create test data"""

        self.business_user1 = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.business_profile1 = Profile.objects.create(user=self.business_user1, type='business')
        self.business_token1 = Token.objects.create(user=self.business_user1)
        
        self.offer = Offer.objects.create(
            creator=self.business_profile1,
            title="Website Design",
            description="Professional website design"
        )
        self.detail1 = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=2,
            delivery_time_in_days=5,
            price=100.00,
            features=["Logo", "Homepage"],
            offer_type="basic"
        )
        self.detail2 = OfferDetail.objects.create(
            offer=self.offer,
            title="Standard",
            revisions=5,
            delivery_time_in_days=7,
            price=200.00,
            features=["Logo", "Homepage", "Contact"],
            offer_type="standard"
        )
        self.detail3 = OfferDetail.objects.create(
            offer=self.offer,
            title="Premium",
            revisions=10,
            delivery_time_in_days=10,
            price=500.00,
            features=["Logo", "Full Website", "SEO"],
            offer_type="premium"
        )
        
    def test_get_offer_detail_authenticated(self):
        """Test retrieving offer details as an authenticated user"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offerdetail-detail', kwargs={'pk': self.detail1.id})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.detail1.id)
        self.assertEqual(response.data['title'], "Basic")
        self.assertEqual(response.data['revisions'], 2)
        self.assertEqual(response.data['delivery_time_in_days'], 5)
        self.assertEqual(float(response.data['price']), 100.00)
        self.assertEqual(response.data['features'], ["Logo", "Homepage"])
        self.assertEqual(response.data['offer_type'], "basic")
        
    def test_get_offer_detail_unauthenticated(self):
        """Test retrieving offer details without authentication"""
        
        url = reverse('offerdetail-detail', kwargs={'pk': self.detail1.id})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_offer_detail_not_found(self):
        """Test retrieving non-existent offer detail"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offerdetail-detail', kwargs={'pk': 999})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        