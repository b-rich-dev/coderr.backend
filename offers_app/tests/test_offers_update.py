from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail


class OfferUpdateTests(APITestCase):
    """Tests for PATCH /api/offers/<id>/"""
    
    def setUp(self):
        """Create test data"""
        
        self.business_user = User.objects.create_user(
            username="business1",
            email="business@example.com",
            password="password123"
        )
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        self.business_token = Token.objects.create(user=self.business_user)
        
        self.offer = Offer.objects.create(
            creator=self.business_profile,
            title="Website Design",
            description="Professional website design"
        )
        
        OfferDetail.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=2,
            delivery_time_in_days=5,
            price=100.00,
            features=["Logo", "Homepage"],
            offer_type="basic"
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Standard",
            revisions=5,
            delivery_time_in_days=7,
            price=200.00,
            features=["Logo", "Homepage", "Contact"],
            offer_type="standard"
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title="Premium",
            revisions=10,
            delivery_time_in_days=10,
            price=500.00,
            features=["Logo", "Full Website", "SEO"],
            offer_type="premium"
        )
    
    def test_update_offer_title_success(self):
        """Test: Successfully update offer title"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        data = {
            "title": "Updated Website Design"
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Website Design')
    
    def test_update_offer_details_with_offer_type_success(self):
        """Test: Successfully update offer details when offer_type is provided"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        data = {
            "details": [
                {
                    "offer_type": "basic",
                    "price": 150.00,
                    "revisions": 3
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        basic_detail = next(d for d in response.data['details'] if d['offer_type'] == 'basic')
        self.assertEqual(float(basic_detail['price']), 150.00)
        self.assertEqual(basic_detail['revisions'], 3)
    
    def test_update_offer_details_without_offer_type_fails(self):
        """Test: Update offer details without offer_type returns 400"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        data = {
            "details": [
                {
                    "price": 150.00,
                    "revisions": 3
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)
    
    def test_update_multiple_details_with_offer_type_success(self):
        """Test: Successfully update multiple details when offer_type is provided for each"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        data = {
            "details": [
                {
                    "offer_type": "basic",
                    "price": 120.00
                },
                {
                    "offer_type": "premium",
                    "price": 550.00
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        basic_detail = next(d for d in response.data['details'] if d['offer_type'] == 'basic')
        premium_detail = next(d for d in response.data['details'] if d['offer_type'] == 'premium')
        
        self.assertEqual(float(basic_detail['price']), 120.00)
        self.assertEqual(float(premium_detail['price']), 550.00)
    
    def test_update_details_mixed_with_and_without_offer_type_fails(self):
        """Test: Update with mixed details (some with, some without offer_type) fails"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        data = {
            "details": [
                {
                    "offer_type": "basic",
                    "price": 120.00
                },
                {
                    "price": 250.00
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)
