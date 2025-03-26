import logging
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Occasion

logger = logging.getLogger(__name__)

class OccasionTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.create_url = reverse('occasion-create')
        cls.occasion_data = {
            'name': 'Birthday Party',
            'date': '2025-03-26',
            'description': 'A birthday celebration.'
        }
        logger.info("Test data setup complete for OccasionTests.")

    def test_create_occasion(self):
        logger.info("Starting test_create_occasion in OccasionTests")
        response = self.client.post(self.create_url, self.occasion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Occasion.objects.count(), 1)
        self.assertEqual(Occasion.objects.get().name, 'Birthday Party')
        logger.info("test_create_occasion completed successfully in OccasionTests")

    def test_create_occasion_missing_name(self):
        logger.info("Starting test_create_occasion_missing_name in OccasionTests")
        invalid_data = self.occasion_data.copy()
        invalid_data['name'] = ''
        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        logger.info("test_create_occasion_missing_name completed successfully in OccasionTests")

    def test_create_occasion_invalid_date(self):
        logger.info("Starting test_create_occasion_invalid_date in OccasionTests")
        invalid_data = self.occasion_data.copy()
        invalid_data['date'] = 'invalid-date'
        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        logger.info("test_create_occasion_invalid_date completed successfully in OccasionTests")