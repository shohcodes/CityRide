from django.urls import path, include

urlpatterns = [
    path('', include("apps.core.urls")),
    path('', include("apps.drivers.urls")),
    path('', include("apps.users.urls")),
    path('', include("apps.orders.urls")),
]
