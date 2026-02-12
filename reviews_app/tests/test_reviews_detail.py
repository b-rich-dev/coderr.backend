from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile
from reviews_app.models import Reviews


class ReviewDetailTests(APITestCase):
    """Tests for GET, PUT, PATCH, DELETE /api/reviews/{id}/ endpoint to manage review details"""
        
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
        
        self.review = Reviews.objects.create(
            business_id=self.business_profile1.id,
            reviewer=self.customer_profile,
            rating=4,
            description="Good service!"
        )
        
    def test_get_review_detail(self):
        """Test retrieving a review detail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review_data = response.data
        self.assertEqual(review_data['business_user'], self.business_user1.id)
        self.assertEqual(review_data['reviewer'], self.customer_user.id)
        self.assertEqual(review_data['rating'], 4)
        self.assertEqual(review_data['description'], "Good service!")
        
    def test_update_review_detail(self):
        """Test updating a review detail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        update_data = {
            'rating': 5,
            'description': "Excellent service!"
        }
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review_data = response.data
        self.assertEqual(review_data['rating'], 5)
        self.assertEqual(review_data['description'], "Excellent service!")
        
    def test_update_review_unauthorized(self):
        """Test updating a review detail without authorization should fail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        update_data = {
            'rating': 5,
            'description': "Excellent service!"
        }
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_not_found(self):
        """Test retrieving a non-existent review should return 404"""
        
        url = reverse('review-detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_review_forbitten(self):
        """Test updating a review by a user who is not the reviewer should fail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        update_data = {
            'rating': 5,
            'description': "Excellent service!"
        }
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_review_wrong_data(self):
        """Test updating a review with wrong data should return 400"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        update_data = {
            'rating': 'invalid',
            'description': "Excellent service!"
        }
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_partial_update(self):
        """Test partially updating a review detail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        update_data = {
            'description': "Updated description only"
        }
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review_data = response.data
        self.assertEqual(review_data['rating'], 4)
        self.assertEqual(review_data['description'], "Updated description only")
     
    def test_delete_review_detail(self):
        """Test deleting a review detail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reviews.objects.filter(id=self.review.id).exists())
        
    def test_delete_review_unauthorized(self):
        """Test deleting a review detail without authorization should fail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_review_forbidden(self):
        """Test deleting a review by a user who is not the reviewer should fail"""
        
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_review_not_found(self):
        """Test deleting a non-existent review should return 404"""
        
        url = reverse('review-detail', kwargs={'pk': 999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        