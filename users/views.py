from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User, Payments
from users.permissions import IsModerator
from users.serliazers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_sessions


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        try:
            payment = serializer.save(user=self.request.user)
            product = create_stripe_product(payment.course or payment.lesson)
            price = create_stripe_price(payment.amount, product)
            session_id, link = create_stripe_sessions(price)
            payment.session_id = session_id
            payment.link = link
            payment.save()
        except serializers.ValidationError("Выберите курс или урок для оплаты") as error:
            return Response({"Error": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_amount",)
