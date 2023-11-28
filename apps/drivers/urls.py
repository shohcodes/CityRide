from rest_framework.routers import DefaultRouter

from apps.drivers.views import DriversViewSet, CarModelViewSet

router = DefaultRouter()

router.register(prefix='drivers', viewset=DriversViewSet, basename='drivers')
router.register(prefix='car_models', viewset=CarModelViewSet, basename='car_models')

urlpatterns = router.urls
