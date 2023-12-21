from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import get_me

urlpatterns = [
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/get_me/', get_me, name='get_me')
]
