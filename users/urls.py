from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, UserListAPIView, PaymentsListAPIView, PaymentsCreateView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('payments/create/', PaymentsCreateView.as_view(), name='payments_create'),
    ]
