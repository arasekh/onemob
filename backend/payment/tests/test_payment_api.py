from django.test import TestCase, override_settings
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.authtoken.models import Token
from django.conf import settings
from virtualclass.models import Student

User = get_user_model()
PAYMENT_URL = reverse('payment_api:create')
BASE_URL = 'http://127.0.0.1:8000/'


def get_authorized_client(user):
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=('{} {}'.format(settings.AUTH_HEADER_PREFIX, token)))
    return client


@override_settings(BASE_URL=BASE_URL, IDPAY_SANDBOX=True)
class PaymentApiTests(TestCase):
    """
        Test connecting to payment api and returning api links.
    """
    def setUp(self):
        self.fake = Faker()

    def test_payment_create_success(self):
        """
            Test making post request to payment_create is successful
        """
        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 1000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def test_payment_create_without_amount(self):
        """
            Test making post request to payment_create without providing amount fails
        """
        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_payment_create_invalid_amount(self):
        """
            Test making post request to payment_create providing and invalid amount fails
        """
        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 0}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, res.status_code)

        payload = {'amount': 500000000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, res.status_code)

    def test_get_payment_link(self):
        """
            Test making request to payment api providing the amount returns the correct link.
        """
        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 1000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertIn('link', res.data)
