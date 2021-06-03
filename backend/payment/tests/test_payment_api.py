from django.test import TestCase, override_settings
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.authtoken.models import Token
from django.conf import settings
from virtualclass.models import Student, Transaction
from unittest import mock

User = get_user_model()
PAYMENT_URL = reverse('payment_api:create')
PAYMENT_RETURN = reverse('payment_api:return')
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
        self.paymentReturnPayload = {
            'status': '10', 'track_id': 466961, 'order_id': '9', 'amount': 1000,
            'id': '8a1079e9f557d75485174f9bafd57f95', 'card_no': '123456******1234',
            'date': '1622721144',
            'hashed_card_no': 'E59FA6241C94B8836E3D03120DF33E80FD988888BBA0A122240C2E7D23B48295'
        }
        self.paymentReturnSuccessExpectedDict = {
            "status": "100",
            "track_id": "10012",
            "id": "d2e353189823079e1e4181772cff5292",
            "order_id": "101",
            "amount": "10000",
            "date": "1546288200",
            "payment": {
                "track_id": "888001",
                "amount": "10000",
                "card_no": "123456******1234",
                "hashed_card_no": "E59FA6241C94B8836E3D03120DF33E80FD988888BBA0A122240C2E7D23B48295",
                "date": "1546288500"
            },
            "verify": {
                "date": "1546288800"
            }
        }

    @mock.patch('idpay.api.requests.post')
    def test_payment_create_success(self, mockPost):
        """
            Test making post request to payment_create is successful
        """
        mockResponse = mock.Mock()
        expectedDict = {
            'id': self.payment_id,
            'link': self.payment_link
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
            'error_code': self.error_code,
            'error_message': self.error_message
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
            'error_code': self.error_code,
            'error_message': self.error_message
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
            'id': self.payment_id,
            'link': self.payment_link
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

    @mock.patch('idpay.api.requests.post')
    def test_payment_return_success(self, mockPost):
        """
            Test these conditions for payment return api:
                1.Response code -> should be 200
                2.Template used -> correct template is returned
                3.Template contains some specific text
                4.User balande is updated
                5.Transaction fields are set and its status is updated to verified
        """
        mockResponse = mock.Mock()
        expectedDict = self.paymentReturnSuccessExpectedDict
        mockResponse.json.return_value = expectedDict
        mockResponse.status_code = 200
        mockPost.return_value = mockResponse

        client = self.client
        payload = self.paymentReturnPayload
        student = Student.objects.create(username='test', password='randompass')
        balance = student.balance
        transaction = Transaction.objects.create(pk=int(payload['order_id']),
                                                 payment_id=payload['id'],
                                                 amount=payload['amount'],
                                                 user=student)
        res = client.post(PAYMENT_RETURN, payload)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertTemplateUsed(res, 'payment/idpay.html')
        self.assertContains(res, 'بازگشت به برنامه')
        self.assertContains(res, 'پرداخت با موفقیت انجام شد.')
        student.refresh_from_db()
        self.assertEqual(balance + int(transaction.amount), student.balance)
        transaction.refresh_from_db()
        self.assertEqual(Transaction.TransactionStatus.verified, transaction.status)
        self.assertEqual(student, transaction.user)
        self.assertEqual(payload['id'], transaction.payment_id)
        self.assertEqual(payload['track_id'], transaction.idpay_track_id)
        self.assertEqual(expectedDict['payment']['track_id'], transaction.bank_track_id)
        self.assertEqual(payload['amount'], transaction.amount)
        self.assertEqual(payload['card_no'], transaction.card_number)
        self.assertEqual(payload['hashed_card_no'], transaction.hashed_card_number)
        self.assertEqual(payload['date'], str(int(transaction.date.timestamp() * 1000)))
