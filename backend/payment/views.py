from virtualclass.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from idpay.api import IDPayAPI
from rest_framework.views import APIView
from django.urls import reverse
from .serializers import PaymentCreateSerializer
from rest_framework import status


def payment_init():
    base_url = settings.BASE_URL
    api_key = settings.IDPAY_API_KEY
    sandbox = settings.IDPAY_SANDBOX
    return IDPayAPI(api_key, base_url, sandbox)


class paymentCreate(APIView):
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
            transaction = serializer.save()
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

            # import pdb; pdb.set_trace()
            if 'id' in result:
                transaction.status = 1
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


class paymentReturn(APIView):
    pass
