from virtualclass.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from idpay.api import IDPayAPI
from rest_framework.views import APIView
from django.urls import reverse
from .serializers import PaymentCreateSerializer
from rest_framework import status
from virtualclass.models import Transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import pytz


def payment_init():
    base_url = settings.BASE_URL
    api_key = settings.IDPAY_API_KEY
    sandbox = settings.IDPAY_SANDBOX
    return IDPayAPI(api_key, base_url, sandbox)


class CreatePayment(APIView):
    serializer_class = PaymentCreateSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = request.auth.user
        # Check Student email verified before doing transaction
        # A normal user must not be able to call this api if his/her email is not verified.
        # TODO

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=student)
            order_id = transaction.pk

            payer = {
                'name': student.first_name,
                'mail': student.email,
                # 'phone': request.POST.get('phone'),
                # 'desc': request.POST.get('desc'),
            }

            idpay_payment = payment_init()
            IDPAY_CALLBACK = reverse('payment_api:return')
            result = idpay_payment.payment(str(order_id), float(transaction.amount),
                                           IDPAY_CALLBACK, payer)

            if 'id' in result:
                transaction.status = Transaction.TransactionStatus.incomplete
                transaction.payment_id = result['id']
                transaction.payment_link = result['link']
                transaction.save()
                return Response({
                    'link': result['link'],
                }, status=status.HTTP_201_CREATED)

            result_dict = {n[0].strip(): n[1].strip() for n in [splits.strip().split(':') for
                           splits in result['message'].split('|')]}
            return Response({
                'detail': result_dict['Description'],
                'idpay_error_code': result_dict['Error Code'],
            }, status=result_dict['Http status Code'])

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _update_balance(transaction):
    user = transaction.user
    user.balance += transaction.amount
    user.save()


def _verify_transaction(request, paymentID, orderID, transaction):
    idpay_payment = payment_init()
    result = idpay_payment.verify(paymentID, orderID)
    if 'status' in result:
        # Transaction verified successfully.
        _update_balance(transaction)
        transaction.status = result['status']
        transaction.bank_track_id = result['payment']['track_id']
        transaction.save()
        return 'پرداخت با موفقیت انجام شد.'
    # Transaction not verified.
    return result['message']


def _get_transaction_status(status):
    states = {
        1: 'پرداخت انجام نشده است.',
        2: 'پرداخت ناموفق بوده است.',
        3: 'خطایی رخ داده است',
        4: 'پرداخت بلوکه شده است.',
        5: 'برگشت به پرداخت کننده',
        6: 'برگشت خورده سیستمی',
        7: 'انصراف از پرداخت',
        8: 'به درگاه پرداخت منتقل شده است.',
        10: 'در انتظار تایید پرداخت',
        100: 'پرداخت تایید شده است.',
        101: 'پرداخت قبلا تایید شده است.',
        200: 'به دریافت کننده واریز شد.',
    }
    if states[int(status)]:
        return states[int(status)]
    return False


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':
        paymentID = request.POST.get('id')
        status = request.POST.get('status')
        idpayTrackID = request.POST.get('track_id')
        orderID = request.POST.get('order_id')
        amount = request.POST.get('amount')
        cardNumber = request.POST.get('card_no')
        hashedCardNumber = request.POST.get('hashed_card_no')
        date = request.POST.get('date')

        queryset = Transaction.objects.filter(pk=int(orderID), payment_id=paymentID,
                                              amount=amount)
        if queryset.count() == 1:
            transaction = queryset[0]
            if transaction.status == Transaction.TransactionStatus.incomplete:
                transaction.status = status
                transaction.date = datetime.fromtimestamp(int(date)/1000, tz=pytz.timezone(
                    settings.TIME_ZONE))
                transaction.card_number = cardNumber
                transaction.hashed_card_number = hashedCardNumber
                transaction.idpay_track_id = idpayTrackID
                transaction.save()
                if int(status) == Transaction.TransactionStatus.verificationPending.value:
                    txt = _verify_transaction(request, paymentID, orderID, transaction)
                else:
                    # Show a proper message according to the response status.
                    txt = _get_transaction_status(status)
            elif transaction.status == Transaction.TransactionStatus.verificationPending:
                # An error has occured during last transaction verification. Try again.
                txt = _verify_transaction(request, paymentID, orderID, transaction)
            else:
                # Double spending
                txt = "متاسفم. این سفارش قبلا ثبت شده است. لطفا یک سفارش جدید ایجاد کنید."
        else:
            txt = "سفارش موردنظر شما یافت نشد!"  # Order Not Found
    else:
        txt = "فکر میکنم راهتون رو گم کردین!"  # Bad Request
    return render(request, 'payment/idpay.html', {'txt': txt})
