from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders


class OrderCountTests(APITestCase):
    """Tests for GET /api/order-count/{business_user_id}/"""
    
    def setUp(self):
        """Create test data"""

        self.customer_user = User.objects.create_user(
            username="customer1",
            email="customer@example.com",
            password="password123"
        )
        self.customer_profile = Profile.objects.create(user=self.customer_user, type='customer')
        self.customer_token = Token.objects.create(user=self.customer_user)
        
        self.business_user1 = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123"
        )
        self.business_profile1 = Profile.objects.create(user=self.business_user1, type='business')
        self.business_token1 = Token.objects.create(user=self.business_user1)
        
        self.business_user2 = User.objects.create_user(
            username="business2",
            email="business2@example.com",
            password="password123"
        )
        self.business_profile2 = Profile.objects.create(user=self.business_user2, type='business')
        self.business_token2 = Token.objects.create(user=self.business_user2)
        
        self.offer1 = Offer.objects.create(
            creator=self.business_profile1,
            title="Website Design",
            description="Professional website design"
        )
        self.offer_detail1 = OfferDetail.objects.create(
            offer=self.offer1,
            title="Basic Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic"
        )
        
        Orders.objects.create(
            offer_detail=self.offer_detail1,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Order 1",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design"],
            offer_type="basic",
            status="in_progress"
        )
        Orders.objects.create(
            offer_detail=self.offer_detail1,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Order 2",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design"],
            offer_type="basic",
            status="in_progress"
        )
        Orders.objects.create(
            offer_detail=self.offer_detail1,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Order 3",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design"],
            offer_type="basic",
            status="completed"
        )
        Orders.objects.create(
            offer_detail=self.offer_detail1,
            customer=self.customer_profile,
            business=self.business_profile1,
            title="Order 4",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design"],
            offer_type="basic",
            status="cancelled"
        )
    
    def test_get_order_count_for_business(self):
        """Test: Get order count for business user with in_progress orders"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-count', kwargs={'business_user_id': self.business_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_count', response.data)
        self.assertEqual(response.data['order_count'], 2)
        
    def test_get_order_count_no_orders(self):
        """Test: Get order count for business user with no orders"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-count', kwargs={'business_user_id': self.business_user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 0)
        
    def test_get_order_count_only_counts_in_progress(self):
        """Test: Order count only includes in_progress status"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('order-count', kwargs={'business_user_id': self.business_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.data['order_count'], 2)
        
    def test_get_order_count_unauthenticated(self):
        """Test: Unauthenticated request returns 401"""
        url = reverse('order-count', kwargs={'business_user_id': self.business_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_order_count_user_not_found(self):
        """Test: Non-existent user returns 404"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-count', kwargs={'business_user_id': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        
    def test_get_order_count_as_business_user(self):
        """Test: Business user can check their own order count"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('order-count', kwargs={'business_user_id': self.business_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)
        
    def test_get_order_count_response_format(self):
        """Test: Response has correct format"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-count', kwargs={'business_user_id': self.business_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('order_count', response.data)
        self.assertIsInstance(response.data['order_count'], int)
