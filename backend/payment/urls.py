from django.urls import path
from .views import paymentCreate, paymentReturn

urlpatterns = [
    path('create/', paymentCreate.as_view(), name='create'),
    path('return/', paymentReturn.as_view(), name='return'),
]