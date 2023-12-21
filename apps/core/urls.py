from django.urls import path

from apps.users.views import get_me

urlpatterns = [
    path('auth/get_me/', get_me, name='get_me')
]
