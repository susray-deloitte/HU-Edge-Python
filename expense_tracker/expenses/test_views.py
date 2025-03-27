import logging
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Occasion, Expenditure, PaymentLog

User = get_user_model()

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

class ExpenditureTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.expender = User.objects.create_user(username='expender', password='password123')
        cls.utilizer1 = User.objects.create_user(username='utilizer1', password='password123')
        cls.utilizer2 = User.objects.create_user(username='utilizer2', password='password123')

        # Create a test occasion
        cls.occasion = Occasion.objects.create(name='Test Occasion', date='2025-03-27', description='Test Description')

        # Define the URL for creating expenditures
        cls.create_url = reverse('expenditure-create')

        logger.info("Test data setup complete for ExpenditureTests.")

    def test_create_expenditure(self):
        logger.info("Starting test_create_expenditure in ExpenditureTests")
        data = {
            'occasion': self.occasion.id,
            'event_name': 'Dinner Party',
            'amount': 150.75,
            'expender': self.expender.id,
            'utilizers': [self.utilizer1.id, self.utilizer2.id]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expenditure.objects.count(), 1)
        expenditure = Expenditure.objects.first()
        self.assertEqual(expenditure.event_name, 'Dinner Party')
        self.assertEqual(expenditure.amount, 150.75)
        self.assertEqual(expenditure.expender, self.expender)
        self.assertEqual(list(expenditure.utilizers.all()), [self.utilizer1, self.utilizer2])
        logger.info("test_create_expenditure completed successfully in ExpenditureTests")

    def test_create_expenditure_invalid_amount(self):
        logger.info("Starting test_create_expenditure_invalid_amount in ExpenditureTests")
        data = {
            'occasion': self.occasion.id,
            'event_name': 'Dinner Party',
            'amount': -50.00,  # Invalid amount
            'expender': self.expender.id,
            'utilizers': [self.utilizer1.id, self.utilizer2.id]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
        logger.info("test_create_expenditure_invalid_amount completed successfully in ExpenditureTests")

    def test_create_expenditure_no_utilizers(self):
        logger.info("Starting test_create_expenditure_no_utilizers in ExpenditureTests")
        data = {
            'occasion': self.occasion.id,
            'event_name': 'Dinner Party',
            'amount': 100.00,
            'expender': self.expender.id,
            'utilizers': []  # No utilizers
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('utilizers', response.data)
        logger.info("test_create_expenditure_no_utilizers completed successfully in ExpenditureTests")

class ClearExpenseTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.expender = User.objects.create_user(username='expender', password='password123')
        cls.utilizer1 = User.objects.create_user(username='utilizer1', password='password123')
        cls.utilizer2 = User.objects.create_user(username='utilizer2', password='password123')

        # Create a test occasion
        cls.occasion = Occasion.objects.create(name='Test Occasion', date='2025-03-27', description='Test Description')

        # Create a test expenditure
        cls.expenditure = Expenditure.objects.create(
            occasion=cls.occasion,
            event_name='Dinner Party',
            amount=150.75,
            expender=cls.expender
        )
        cls.expenditure.utilizers.set([cls.utilizer1, cls.utilizer2])

        # Define the URL for clearing expenses
        cls.clear_expense_url = reverse('clear-expense')

        logger.info("Test data setup complete for ClearExpenseTests.")

    def test_clear_expense_success(self):
        logger.info("Starting test_clear_expense_success in ClearExpenseTests")
        data = {
            'expenditure_id': self.expenditure.id,
            'payer_id': self.utilizer1.id,
            'amount': 150.75
        }
        response = self.client.post(self.clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PaymentLog.objects.count(), 1)
        payment_log = PaymentLog.objects.first()
        self.assertEqual(payment_log.payer, self.utilizer1)
        self.assertEqual(payment_log.payee, self.expender)
        self.assertEqual(payment_log.amount, 150.75)
        self.assertTrue(Expenditure.objects.get(id=self.expenditure.id).cleared)
        logger.info("test_clear_expense_success completed successfully in ClearExpenseTests")

    def test_clear_expense_invalid_amount(self):
        logger.info("Starting test_clear_expense_invalid_amount in ClearExpenseTests")
        data = {
            'expenditure_id': self.expenditure.id,
            'payer_id': self.utilizer1.id,
            'amount': 100.00  # Incorrect amount
        }
        response = self.client.post(self.clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(PaymentLog.objects.count(), 0)
        self.assertFalse(Expenditure.objects.get(id=self.expenditure.id).cleared)
        logger.info("test_clear_expense_invalid_amount completed successfully in ClearExpenseTests")

    def test_clear_expense_invalid_payer(self):
        logger.info("Starting test_clear_expense_invalid_payer in ClearExpenseTests")
        data = {
            'expenditure_id': self.expenditure.id,
            'payer_id': self.expender.id,  # Expender cannot be the payer
            'amount': 150.75
        }
        response = self.client.post(self.clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(PaymentLog.objects.count(), 0)
        self.assertFalse(Expenditure.objects.get(id=self.expenditure.id).cleared)
        logger.info("test_clear_expense_invalid_payer completed successfully in ClearExpenseTests")

    def test_clear_expense_already_cleared(self):
        logger.info("Starting test_clear_expense_already_cleared in ClearExpenseTests")
        # First, clear the expense
        data = {
            'expenditure_id': self.expenditure.id,
            'payer_id': self.utilizer1.id,
            'amount': 150.75
        }
        self.client.post(self.clear_expense_url, data, format='json')

        # Attempt to clear the same expense again
        response = self.client.post(self.clear_expense_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(PaymentLog.objects.count(), 1)  # Only one payment log should exist
        logger.info("test_clear_expense_already_cleared completed successfully in ClearExpenseTests")

class ViewOccasionSummaryTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.expender1 = User.objects.create_user(username='expender1', password='password123')
        cls.expender2 = User.objects.create_user(username='expender2', password='password123')
        cls.utilizer1 = User.objects.create_user(username='utilizer1', password='password123')
        cls.utilizer2 = User.objects.create_user(username='utilizer2', password='password123')

        # Create a test occasion
        cls.occasion = Occasion.objects.create(name='Birthday Party', date='2025-03-27', description='A birthday celebration.')

        # Create test expenditures
        cls.expenditure1 = Expenditure.objects.create(
            occasion=cls.occasion,
            event_name='Dinner',
            amount=150.25,
            expender=cls.expender1,
            cleared=True
        )
        cls.expenditure1.utilizers.set([cls.utilizer1, cls.utilizer2])

        cls.expenditure2 = Expenditure.objects.create(
            occasion=cls.occasion,
            event_name='Drinks',
            amount=150.25,
            expender=cls.expender2,
            cleared=False
        )
        cls.expenditure2.utilizers.set([cls.utilizer1, cls.utilizer2])

        # Define the URL for viewing the occasion summary
        cls.occasion_summary_url = reverse('occasion-summary', kwargs={'pk': cls.occasion.id})

        logger.info("Test data setup complete for ViewOccasionSummaryTests.")

    def test_view_occasion_summary_success(self):
        logger.info("Starting test_view_occasion_summary_success in ViewOccasionSummaryTests")
        response = self.client.get(self.occasion_summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertIn('total_amount', response.data)
        self.assertIn('expenditures', response.data)
        self.assertEqual(response.data['name'], 'Birthday Party')
        self.assertEqual(response.data['total_amount'], 300.50)
        self.assertEqual(len(response.data['expenditures']), 2)
        logger.info("test_view_occasion_summary_success completed successfully in ViewOccasionSummaryTests")

    def test_view_occasion_summary_not_found(self):
        logger.info("Starting test_view_occasion_summary_not_found in ViewOccasionSummaryTests")
        invalid_url = reverse('occasion-summary', kwargs={'pk': 999})  # Non-existent occasion ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)  # Check for 'error' field
        self.assertEqual(response.data['error'], 'Occasion not found.')  # Custom error message
        logger.info("test_view_occasion_summary_not_found completed successfully in ViewOccasionSummaryTests")