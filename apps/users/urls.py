from django.urls import path
from rest_framework import routers

from apps.users.views import UsersViewSet, VerifyUsersAPIView, ResetPasswordAPIView, ConfirmResetPasswordAPIView, \
    CustomTokenObtainPairView

router = routers.DefaultRouter()

router.register(prefix='users', viewset=UsersViewSet, basename='users')

urlpatterns = [
    path('auth/verify_user/', VerifyUsersAPIView.as_view(), name='verify_user'),
    path('auth/reset_password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('auth/confirm_reset_password/', ConfirmResetPasswordAPIView.as_view(), name='confirm_reset_password'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
] + router.urls
