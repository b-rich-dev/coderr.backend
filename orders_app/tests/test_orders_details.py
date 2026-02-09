from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders


class PatchOrderTests(APITestCase):
    """Tests for PATCH /api/orders/{id}/"""
    
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
        
        # Business User (owner of the order)
        self.business_user = User.objects.create_user(
            username="business1",
            email="business1@example.com",
            password="password123"
        )
        self.business_profile = Profile.objects.create(user=self.business_user, type='business')
        self.business_token = Token.objects.create(user=self.business_user)
        
        # Another Business User (not involved in the order)
        self.business_user2 = User.objects.create_user(
            username="business2",
            email="business2@example.com",
            password="password123"
        )
        self.business_profile2 = Profile.objects.create(user=self.business_user2, type='business')
        self.business_token2 = Token.objects.create(user=self.business_user2)
        
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
        
        # Create Order
        self.order = Orders.objects.create(
            offer_detail=self.offer_detail,
            customer=self.customer_profile,
            business=self.business_profile,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic",
            status="in_progress"
        )
    
    def test_update_order_status_as_business(self):
        """Test: Business user can update order status"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(response.data['status'], 'completed')
        self.assertEqual(response.data['customer_user'], self.customer_user.id)
        self.assertEqual(response.data['business_user'], self.business_user.id)
        self.assertEqual(response.data['title'], 'Logo Design')
        self.assertIn('updated_at', response.data)
        self.assertIn('created_at', response.data)
        
        # Verify in database
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')
        
    def test_update_order_status_to_cancelled(self):
        """Test: Update status to cancelled"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'cancelled'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cancelled')
        
    def test_update_order_status_as_customer_forbidden(self):
        """Test: Customer cannot update order status"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_order_status_as_different_business_forbidden(self):
        """Test: Business user not involved in order cannot update it"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_order_status_unauthenticated(self):
        """Test: Unauthenticated request returns 401"""
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_order_not_found(self):
        """Test: Non-existent order returns 404"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': 99999})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_order_invalid_status(self):
        """Test: Invalid status value returns 400"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'invalid_status'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_order_response_contains_all_fields(self):
        """Test: Response contains all required fields"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertIn('id', response.data)
        self.assertIn('customer_user', response.data)
        self.assertIn('business_user', response.data)
        self.assertIn('title', response.data)
        self.assertIn('revisions', response.data)
        self.assertIn('delivery_time_in_days', response.data)
        self.assertIn('price', response.data)
        self.assertIn('features', response.data)
        self.assertIn('offer_type', response.data)
        self.assertIn('status', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
