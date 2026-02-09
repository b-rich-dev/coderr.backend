from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders


class GetOrdersTests(APITestCase):
    """Tests for GET /api/orders/"""
    
    def setUp(self):
        """Create test data"""
        # Customer User
        self.customer_user = User.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="password123"
        )
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)
        
        # Business User 1
        self.business_user1 = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123"
        )
        self.business_profile1 = Profile.objects.create(user=self.business_user1, type='business')
        self.business_token1 = Token.objects.create(user=self.business_user1)
        
        # Business User 2 (not involved in any order)
        self.business_user2 = User.objects.create_user(
            username="business2",
            email="business2@example.com",
            password="password123"
        )
        self.business_profile2 = Profile.objects.create(user=self.business_user2, type='business')
        self.business_token2 = Token.objects.create(user=self.business_user2)
        
        # Create Offer and OfferDetail
        self.offer = Offer.objects.create(
            creator=self.business_profile1,
            title="Website Design",
            description="Professional website design"
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic"
        )
        
        # Create Orders
        self.order1 = Orders.objects.create(
            offer_detail=self.offer_detail,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Basic Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="in_progress"
        )
        self.order2 = Orders.objects.create(
            offer_detail=self.offer_detail,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Premium Package",
            revisions=10,
            delivery_time_in_days=10,
            price=500.00,
            features=["Full Website", "SEO"],
            offer_type="premium",
            status="completed"
        )
    
    def test_get_orders_as_customer(self):
        """Test: Customer can see their orders"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_get_orders_as_business(self):
        """Test: Business user can see orders where they are the provider"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('orders-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_get_orders_only_own_orders(self):
        """Test: Users only see their own orders"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        url = reverse('orders-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_get_orders_contains_required_fields(self):
        """Test: Order contains all required fields"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        response = self.client.get(url)
        
        order = response.data[0]
        self.assertIn('id', order)
        self.assertIn('customer_user', order)
        self.assertIn('business_user', order)
        self.assertIn('title', order)
        self.assertIn('revisions', order)
        self.assertIn('delivery_time_in_days', order)
        self.assertIn('price', order)
        self.assertIn('features', order)
        self.assertIn('offer_type', order)
        self.assertIn('status', order)
        self.assertIn('created_at', order)
        self.assertIn('updated_at', order)
        
    def test_get_orders_unauthenticated(self):
        """Test: Unauthenticated request returns 401"""
        url = reverse('orders-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostOrdersTests(APITestCase):
    """Tests for POST /api/orders/"""
    
    def setUp(self):
        """Create test data"""
        # Customer User
        self.customer_user = User.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="password123"
        )
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)
        
        # Business User
        self.business_user = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123"
        )
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        self.business_token = Token.objects.create(user=self.business_user)
        
        # Create Offer and OfferDetail
        self.offer = Offer.objects.create(
            creator=self.business_profile,
            title="Website Design",
            description="Professional website design"
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic"
        )
    
    def test_create_order_as_customer(self):
        """Test: Customer can create an order"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        
        data = {
            'offer_detail_id': self.offer_detail.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Basic Package')
        self.assertEqual(response.data['revisions'], 3)
        self.assertEqual(response.data['delivery_time_in_days'], 5)
        self.assertEqual(float(response.data['price']), 150.00)
        self.assertEqual(response.data['features'], ["Logo Design", "Visitenkarten"])
        self.assertEqual(response.data['offer_type'], 'basic')
        self.assertEqual(response.data['status'], 'in_progress')
        self.assertEqual(response.data['customer_user'], self.customer_user.id)
        self.assertEqual(response.data['business_user'], self.business_user.id)
        
    def test_create_order_snapshot_data(self):
        """Test: Order contains snapshot of offer detail data"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        
        data = {
            'offer_detail_id': self.offer_detail.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # Verify order was created in database
        order = Orders.objects.get(id=response.data['id'])
        self.assertEqual(order.title, 'Basic Package')
        self.assertEqual(order.revisions, 3)
        self.assertEqual(order.delivery_time_in_days, 5)
        self.assertEqual(float(order.price), 150.00)
        self.assertEqual(order.customer, self.customer_profile)
        self.assertEqual(order.business, self.business_profile)
        
    def test_create_order_as_business_forbidden(self):
        """Test: Business user cannot create orders"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('orders-list-create')
        
        data = {
            'offer_detail_id': self.offer_detail.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_order_unauthenticated(self):
        """Test: Unauthenticated request returns 401"""
        url = reverse('orders-list-create')
        
        data = {
            'offer_detail_id': self.offer_detail.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_order_invalid_offer_detail_id(self):
        """Test: Invalid offer detail ID returns 404"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        
        data = {
            'offer_detail_id': 99999
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_order_missing_offer_detail_id(self):
        """Test: Missing offer detail ID returns 400"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('orders-list-create')
        
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('offer_detail_id', response.data)
    
