from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, UserListAPIView, PaymentsListAPIView, PaymentsCreateAPIView, UserCreateAPIView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('users/create/', UserCreateAPIView.as_view(), name='users_create'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments_create'),
]
