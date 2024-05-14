from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserViewSet,
    UserListAPIView,
    PaymentsListAPIView,
    PaymentsCreateAPIView,
    UserCreateAPIView,
)

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")

app_name = UsersConfig.name

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
]
