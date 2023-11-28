from django.urls import path
from rest_framework import routers

from apps.users.views import UsersViewSet, VerifyUsersAPIView, ResetPasswordAPIView, ConfirmResetPasswordAPIView

router = routers.DefaultRouter()

router.register(prefix='users', viewset=UsersViewSet, basename='users')

urlpatterns = [
    path('verify_user/', VerifyUsersAPIView.as_view(), name='verify_user'),
    path('reset_password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('confirm_reset_password/', ConfirmResetPasswordAPIView.as_view(), name='confirm_reset_password')
] + router.urls
