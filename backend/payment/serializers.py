from rest_framework import serializers
from virtualclass.models import Transaction


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', )
