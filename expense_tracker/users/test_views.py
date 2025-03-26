import logging
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

class UserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('register')
        cls.login_url = reverse('token_obtain_pair')
        cls.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        cls.user = User.objects.create_user(**cls.user_data)
        logger.info("Test data setup complete for UserTests.")

    def test_user_registration(self):
        logger.info("Starting test_user_registration in UserTests")
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')
        logger.info("test_user_registration completed successfully in UserTests.")

    def test_user_login(self):
        logger.info("Starting test_user_login in UserTests")
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        logger.info("test_user_login completed successfully in UserTests.")

    def test_invalid_user_login(self):
        logger.info("Starting test_invalid_user_login in UserTests")
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        logger.info("test_invalid_user_login completed successfully in UserTests.")