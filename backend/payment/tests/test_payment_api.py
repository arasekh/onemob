from django.test import TestCase, override_settings
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.authtoken.models import Token
from django.conf import settings
from virtualclass.models import Student
from unittest import mock

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
        self.client = APIClient()
        self.fake = Faker()
        self.payment_id = 'd2e353189823079e1e4181772cff5292'
        self.payment_link = 'https://idpay.ir/p/ws-sandbox/d2e353189823079e1e4181772cff5292'
        self.error_code = 32
        self.error_message = 'شماره سفارش `order_id` نباید خالی باشد.'

    @mock.patch('idpay.api.requests.post')
    def test_payment_create_success(self, mockPost):
        """
            Test making post request to payment_create is successful
        """
        mockResponse = mock.Mock()
        expectedDict = {
            "id": self.payment_id,
            "link": self.payment_link
        }
        mockResponse.json.return_value = expectedDict
        mockResponse.status_code = 201
        mockPost.return_value = mockResponse

        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 1000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    @mock.patch('idpay.api.requests.post')
    def test_payment_create_without_amount(self, mockPost):
        """
            Test making post request to payment_create without providing amount fails
        """
        mockResponse = mock.Mock()
        expectedDict = {
            "error_code": self.error_code,
            "error_message": self.error_message
        }
        mockResponse.json.return_value = expectedDict
        mockResponse.status_code = 400
        mockPost.return_value = mockResponse

        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    @mock.patch('idpay.api.requests.post')
    def test_payment_create_invalid_amount(self, mockPost):
        """
            Test making post request to payment_create providing and invalid amount fails
        """
        mockResponse = mock.Mock()
        expectedDict = {
            "error_code": self.error_code,
            "error_message": self.error_message
        }
        mockResponse.json.return_value = expectedDict
        mockResponse.status_code = 406
        mockPost.return_value = mockResponse

        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 0}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, res.status_code)

        payload = {'amount': 500000000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, res.status_code)

    @mock.patch('idpay.api.requests.post')
    def test_payment_create_matches(self, mockPost):
        """
            Test making request to payment api providing the amount returns the correct link.
        """
        mockResponse = mock.Mock()
        expectedDict = {
            "id": self.payment_id,
            "link": self.payment_link
        }
        mockResponse.json.return_value = expectedDict
        mockResponse.status_code = 201
        mockPost.return_value = mockResponse

        student = Student.objects.create(username='test', password='randompass')
        client = get_authorized_client(student)
        payload = {'amount': 1000}
        res = client.post(PAYMENT_URL, payload)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertIn('link', res.data)
        self.assertEqual(expectedDict['link'], res.data['link'])

    # def test_
