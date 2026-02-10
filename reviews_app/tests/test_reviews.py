from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile
from reviews_app.models import Reviews


class ReviewsTests(APITestCase):
        
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
        
    def test_get_reviews(self):
        """Test retrieving reviews for a business user"""
        Reviews.objects.create(
            business_id=self.business_profile1.id,
            reviewer=self.customer_profile,
            rating=5,
            description="Excellent service!"
        )
        
        url = reverse('reviews-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        review_data = response.data[0]
        self.assertEqual(review_data['business_user'], self.business_user1.id)
        self.assertEqual(review_data['reviewer'], self.customer_user.id)
        self.assertEqual(review_data['rating'], '5.0')
        self.assertEqual(review_data['description'], "Excellent service!")    
        
    def test_get_reviews_unauthenticated(self):
        """Test retrieving reviews without authentication should fail"""
        url = reverse('reviews-list-create')
        response = self.client.get(url, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_review(self):
        """Test creating a review for a business user"""
        url = reverse('reviews-list-create')
        data = {
            "business_user": self.business_user1.id,
            "rating": 4,
            "description": "Great service!"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reviews.objects.count(), 1)
        review = Reviews.objects.first()
        self.assertEqual(review.business_id, self.business_profile1.id)
        self.assertEqual(review.reviewer.user.id, self.customer_user.id)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.description, "Great service!")
        
    def test_create_review_unauthenticated(self):
        """Test creating a review without authentication should fail"""
        url = reverse('reviews-list-create')
        data = {
            "business_user": self.business_user1.id,
            "rating": 4,
            "description": "Great service!"
        }
        
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Reviews.objects.count(), 0)
        
    def test_create_review_non_customer(self):
        """Test creating a review as a non-customer user should fail"""
        url = reverse('reviews-list-create')
        data = {
            "business_user": self.business_user1.id,
            "rating": 4,
            "description": "Great service!"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Reviews.objects.count(), 0)
        
    def test_create_review_for_nonexistent_business(self):
        """Test creating a review for a non-existent business user should fail"""
        url = reverse('reviews-list-create')
        data = {
            "business_user": 999, 
            "rating": 4,
            "description": "Great service!"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response = self.client.post(url, data, format='json')
        
        print(f"\n📩 Response Status: {response.status_code}")
        print(f"📦 Response Data: {response.data}\n")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reviews.objects.count(), 0)
        
    def test_create_duplicate_review(self):
        """Test that a reviewer cannot submit multiple reviews for the same business user"""
        url = reverse('reviews-list-create')
        data = {
            "business_user": self.business_user1.id,
            "rating": 4,
            "description": "Great service!"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response1 = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        
        print(f"\n📩 First Response Status: {response1.status_code}")
        print(f"📦 First Response Data: {response1.data}\n")
        print(f"📩 Second Response Status: {response2.status_code}")
        print(f"📦 Second Response Data: {response2.data}\n")
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reviews.objects.count(), 1)
        
    def test_create_review_for_different_business(self):
        """Test that a reviewer can submit reviews for different business users"""
        url = reverse('reviews-list-create')
        data1 = {
            "business_user": self.business_user1.id,
            "rating": 4,
            "description": "Great service!"
        }
        data2 = {
            "business_user": self.business_user2.id,
            "rating": 5,
            "description": "Excellent service!"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        response1 = self.client.post(url, data1, format='json')
        response2 = self.client.post(url, data2, format='json')
        
        print(f"\n📩 First Response Status: {response1.status_code}")
        print(f"📦 First Response Data: {response1.data}\n")
        print(f"📩 Second Response Status: {response2.status_code}")
        print(f"📦 Second Response Data: {response2.data}\n")
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reviews.objects.count(), 2)
        