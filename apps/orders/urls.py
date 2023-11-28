from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.orders.views import DriverOrdersViewSet, ClientOrdersViewSet, ClientOrderAcceptViewSet

router = DefaultRouter()

router.register(prefix='driver-order', viewset=DriverOrdersViewSet, basename='driver-order')
router.register(prefix='client-order', viewset=ClientOrdersViewSet, basename='client-order')
# router.register(prefix='client-order-accept', viewset=ClientOrderAcceptViewSet, basename='client-order-accept')

urlpatterns = [
    path('client-orders/<int:pk>/update/', ClientOrderAcceptViewSet.as_view(), name='client-order-update'),
              ] + router.urls
