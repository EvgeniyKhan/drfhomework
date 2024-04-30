from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    model = Payments
    fields = '__all__'
