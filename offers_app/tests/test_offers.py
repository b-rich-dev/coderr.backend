from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail


class OfferListTests(APITestCase):
    """Tests for GET /api/offers/"""
    
    def setUp(self):
        """Create test data"""

        self.business_user = User.objects.create_user(
            username="business1",
            email="business@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        
        self.offer1 = Offer.objects.create(
            creator=self.business_profile,
            title="Website Design",
            description="Professional website design"
        )
        OfferDetail.objects.create(
            offer=self.offer1,
            title="Basic",
            revisions=2,
            delivery_time_in_days=5,
            price=100.00,
            features=["Logo", "Homepage"],
            offer_type="basic"
        )
        OfferDetail.objects.create(
            offer=self.offer1,
            title="Standard",
            revisions=5,
            delivery_time_in_days=7,
            price=200.00,
            features=["Logo", "Homepage", "Contact"],
            offer_type="standard"
        )
        OfferDetail.objects.create(
            offer=self.offer1,
            title="Premium",
            revisions=10,
            delivery_time_in_days=10,
            price=500.00,
            features=["Logo", "Full Website", "SEO"],
            offer_type="premium"
        )
        
        self.offer2 = Offer.objects.create(
            creator=self.business_profile,
            title="Logo Design",
            description="Creative logo design"
        )
        OfferDetail.objects.create(
            offer=self.offer2,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price=50.00,
            features=["1 Logo concept"],
            offer_type="basic"
        )
        OfferDetail.objects.create(
            offer=self.offer2,
            title="Standard",
            revisions=3,
            delivery_time_in_days=5,
            price=100.00,
            features=["3 Logo concepts"],
            offer_type="standard"
        )
        OfferDetail.objects.create(
            offer=self.offer2,
            title="Premium",
            revisions=5,
            delivery_time_in_days=7,
            price=200.00,
            features=["5 Logo concepts", "Source files"],
            offer_type="premium"
        )
    
    def test_get_offers_list(self):
        """Test: Retrieve offers list"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_offer_contains_required_fields(self):
        """Test: Offer contains all required fields"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        offer = response.data['results'][0]
        self.assertIn('id', offer)
        self.assertIn('user', offer)
        self.assertIn('title', offer)
        self.assertIn('description', offer)
        self.assertIn('created_at', offer)
        self.assertIn('updated_at', offer)
        self.assertIn('details', offer)
        self.assertIn('min_price', offer)
        self.assertIn('min_delivery_time', offer)
        self.assertIn('user_details', offer)
        
    def test_details_format_in_list(self):
        """Test: Details have the correct format (id and url)"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        details = response.data['results'][0]['details']
        self.assertEqual(len(details), 3)
        self.assertIn('id', details[0])
        self.assertIn('url', details[0])
        self.assertTrue(details[0]['url'].startswith('/offerdetails/'))
        
    def test_min_price_calculation(self):
        """Test: min_price is calculated correctly"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        offer = next(o for o in response.data['results'] if o['title'] == 'Website Design')
        self.assertEqual(float(offer['min_price']), 100.00)
        
        offer = next(o for o in response.data['results'] if o['title'] == 'Logo Design')
        self.assertEqual(float(offer['min_price']), 50.00)
        
    def test_min_delivery_time_calculation(self):
        """Test: min_delivery_time is calculated correctly"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        offer = next(o for o in response.data['results'] if o['title'] == 'Website Design')
        self.assertEqual(offer['min_delivery_time'], 5)
        
    def test_user_details_format(self):
        """Test: user_details has the correct format"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url)
        
        user_details = response.data['results'][0]['user_details']
        self.assertEqual(user_details['first_name'], 'John')
        self.assertEqual(user_details['last_name'], 'Doe')
        self.assertEqual(user_details['username'], 'business1')
        
    def test_filter_by_creator_id(self):
        """Test: Filter by creator_id"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'creator_id': self.business_user.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_filter_by_min_price(self):
        """Test: Filter by min_price"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'min_price': 100})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Website Design')
        
    def test_filter_by_max_delivery_time(self):
        """Test: Filter by max_delivery_time"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'max_delivery_time': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Logo Design')
        
    def test_search_in_title(self):
        """Test: Search in title"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'search': 'Website'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Website Design')
        
    def test_search_in_description(self):
        """Test: Search in description"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'search': 'Creative'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Logo Design')
        
    def test_ordering_by_min_price(self):
        """Test: Ordering by min_price"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'ordering': 'min_price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Logo Design')
        self.assertEqual(response.data['results'][1]['title'], 'Website Design')
        
    def test_pagination_page_size(self):
        """Test: Pagination with page_size parameter"""
        
        url = reverse('offers-list-create')
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 2)
        self.assertIsNotNone(response.data['next'])


class OfferCreateTests(APITestCase):
    """Tests for POST /api/offers/"""
    
    def setUp(self):
        """Creates test users"""

        self.business_user = User.objects.create_user(
            username="business1",
            email="business@example.com",
            password="password123"
        )
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        self.business_token = Token.objects.create(user=self.business_user)
        
        self.customer_user = User.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="password123"
        )
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)
        
        self.valid_offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }
    
    def test_create_offer_success(self):
        """Test: Successful creation of an offer as a Business User"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offers-list-create')
        response = self.client.post(url, self.valid_offer_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], 'Grafikdesign-Paket')
        self.assertEqual(len(response.data['details']), 3)
        
        for detail in response.data['details']:
            self.assertIn('id', detail)
            self.assertIn('title', detail)
            self.assertIn('price', detail)
            self.assertIn('features', detail)
    
    def test_create_offer_unauthenticated(self):
        """Test: Creating without authentication returns 401"""
        
        url = reverse('offers-list-create')
        response = self.client.post(url, self.valid_offer_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_offer_customer_user_forbidden(self):
        """Test: Customer User is not allowed to create offers (403)"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('offers-list-create')
        response = self.client.post(url, self.valid_offer_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_offer_less_than_3_details(self):
        """Test: Offer with less than 3 details returns 400"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        invalid_data = self.valid_offer_data.copy()
        invalid_data['details'] = invalid_data['details'][:2] 
        
        url = reverse('offers-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_offer_more_than_3_details(self):
        """Test: Offer with more than 3 details returns 400"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        invalid_data = self.valid_offer_data.copy()
        invalid_data['details'].append({
            "title": "Extra",
            "revisions": 1,
            "delivery_time_in_days": 1,
            "price": 50,
            "features": ["Extra"],
            "offer_type": "basic"
        })
        
        url = reverse('offers-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_offer_missing_required_fields(self):
        """Test: Missing required fields return 400"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        invalid_data = {
            "title": "Test",
            # description is missing
            "details": self.valid_offer_data['details']
        }
        
        url = reverse('offers-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_created_offer_has_correct_creator(self):
        """Test: Created offer has the correct creator"""
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offers-list-create')
        response = self.client.post(url, self.valid_offer_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        offer = Offer.objects.get(id=response.data['id'])
        self.assertEqual(offer.creator, self.business_profile)
