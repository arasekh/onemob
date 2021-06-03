from django.urls import path
from .views import CreatePayment, payment_return

urlpatterns = [
    path('create/', CreatePayment.as_view(), name='create'),
    path('return/', payment_return, name='return'),
]
