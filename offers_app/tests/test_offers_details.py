from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail



class OfferDetailViewTests(APITestCase):
    """Tests for GET/PUT/PATCH/DELETE /api/offers/<id>/"""
    
    def setUp(self):
        """Create test data"""
        # Business User 1
        self.business_user1 = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.business_profile1 = Profile.objects.create(user=self.business_user1, type='business')
        self.business_token1 = Token.objects.create(user=self.business_user1)
        
        # Business User 2
        self.business_user2 = User.objects.create_user(
            username="business2",
            email="business2@example.com",
            password="password123"
        )
        self.business_profile2 = Profile.objects.create(user=self.business_user2, type='business')
        self.business_token2 = Token.objects.create(user=self.business_user2)
        
        # Customer User
        self.customer_user = User.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="password123"
        )
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)
        
        # Create test offer
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
        """Test: Retrieve single offer detail as authenticated user"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.offer.id)
        self.assertEqual(response.data['title'], 'Website Design')
        self.assertEqual(response.data['user'], self.business_user1.id)
        
    def test_get_offer_detail_has_all_fields(self):
        """Test: Offer detail contains all required fields"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertIn('id', response.data)
        self.assertIn('user', response.data)
        self.assertIn('title', response.data)
        self.assertIn('image', response.data)
        self.assertIn('description', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        self.assertIn('details', response.data)
        self.assertIn('min_price', response.data)
        self.assertIn('min_delivery_time', response.data)
        
    def test_get_offer_detail_shows_details_with_id_and_url(self):
        """Test: Details in offer detail have id and url format"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertEqual(len(response.data['details']), 3)
        detail = response.data['details'][0]
        self.assertIn('id', detail)
        self.assertIn('url', detail)
        self.assertTrue(detail['url'].startswith('/offerdetails/'))
        
    def test_get_offer_detail_calculates_min_price(self):
        """Test: min_price is calculated correctly"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertEqual(float(response.data['min_price']), 100.00)
        
    def test_get_offer_detail_calculates_min_delivery_time(self):
        """Test: min_delivery_time is calculated correctly"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertEqual(response.data['min_delivery_time'], 5)
        
    def test_get_offer_detail_unauthenticated(self):
        """Test: Unauthenticated request returns 401"""
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_offer_detail_not_found(self):
        """Test: Non-existent offer returns 404"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offer-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_offer_authenticated(self):
        """Test: Update offer as authenticated user (owner)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        update_data = {
            'title': 'Updated Website Design',
            'description': 'Updated description'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Website Design')
        self.assertEqual(response.data['description'], 'Updated description')
        
        # Verify in database
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, 'Updated Website Design')
        self.assertEqual(self.offer.description, 'Updated description')
        
    def test_update_offer_with_details_by_offer_type(self):
        """Test: Update specific detail by offer_type"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        update_data = {
            'title': 'Updated Website Design',
            'details': [
                {
                    'title': 'Basic Design Updated',
                    'revisions': 3,
                    'delivery_time_in_days': 6,
                    'price': 120,
                    'features': ['Logo Design', 'Flyer'],
                    'offer_type': 'basic'
                }
            ]
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Website Design')
        
        # Verify all details are returned
        self.assertEqual(len(response.data['details']), 3)
        
        # Find and verify the updated basic detail
        basic_detail = next(d for d in response.data['details'] if d['offer_type'] == 'basic')
        self.assertEqual(basic_detail['title'], 'Basic Design Updated')
        self.assertEqual(basic_detail['revisions'], 3)
        self.assertEqual(basic_detail['delivery_time_in_days'], 6)
        self.assertEqual(float(basic_detail['price']), 120.00)
        self.assertEqual(basic_detail['features'], ['Logo Design', 'Flyer'])
        
        # Verify other details remain unchanged
        standard_detail = next(d for d in response.data['details'] if d['offer_type'] == 'standard')
        self.assertEqual(standard_detail['title'], 'Standard')
        self.assertEqual(standard_detail['revisions'], 5)
        
        premium_detail = next(d for d in response.data['details'] if d['offer_type'] == 'premium')
        self.assertEqual(premium_detail['title'], 'Premium')
        self.assertEqual(premium_detail['revisions'], 10)
        
    def test_update_multiple_details_by_offer_type(self):
        """Test: Update multiple details in one request"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        update_data = {
            'details': [
                {
                    'title': 'Basic Updated',
                    'price': 110,
                    'offer_type': 'basic'
                },
                {
                    'title': 'Premium Updated',
                    'price': 550,
                    'offer_type': 'premium'
                }
            ]
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify basic and premium were updated
        basic_detail = next(d for d in response.data['details'] if d['offer_type'] == 'basic')
        self.assertEqual(basic_detail['title'], 'Basic Updated')
        self.assertEqual(float(basic_detail['price']), 110.00)
        
        premium_detail = next(d for d in response.data['details'] if d['offer_type'] == 'premium')
        self.assertEqual(premium_detail['title'], 'Premium Updated')
        self.assertEqual(float(premium_detail['price']), 550.00)
        
        # Verify standard was not changed
        standard_detail = next(d for d in response.data['details'] if d['offer_type'] == 'standard')
        self.assertEqual(standard_detail['title'], 'Standard')
        self.assertEqual(float(standard_detail['price']), 200.00)
        
    def test_update_offer_not_owner_forbidden(self):
        """Test: Update offer as non-owner returns 403"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        update_data = {'title': 'Hacked Title'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify offer was not changed
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, 'Website Design')
        
    def test_update_offer_unauthenticated(self):
        """Test: Update offer without authentication returns 401"""
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        update_data = {'title': 'Updated'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_offer_authenticated(self):
        """Test: Delete offer as owner"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        self.assertFalse(Offer.objects.filter(id=self.offer.id).exists())
        
    def test_delete_offer_not_owner_forbidden(self):
        """Test: Delete offer as non-owner returns 403"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify offer still exists
        self.assertTrue(Offer.objects.filter(id=self.offer.id).exists())
        
    def test_delete_offer_unauthenticated(self):
        """Test: Delete offer without authentication returns 401"""
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify offer still exists
        self.assertTrue(Offer.objects.filter(id=self.offer.id).exists())
