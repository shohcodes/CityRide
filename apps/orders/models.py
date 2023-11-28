from django.db import models

from apps.core.models import TimeStampedModel
from apps.drivers.models import Drivers
from apps.users.models import User


class DriverOrders(TimeStampedModel):
    driver = models.ForeignKey(User, related_name='drivers_order', on_delete=models.CASCADE)
    fromm = models.CharField(max_length=255)
    to = models.CharField(max_length=255)
    time = models.DateTimeField()
    price = models.IntegerField()
    seats = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'DriverOrder'
        verbose_name_plural = 'DriverOrders'

    def __str__(self):
        return f'{self.driver}'


class ClientOrder(TimeStampedModel):
    client = models.ForeignKey(User, related_name='client_order', on_delete=models.CASCADE)
    driver_order = models.ForeignKey(DriverOrders, related_name='client_driver_order', on_delete=models.CASCADE)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ClientOrder'
        verbose_name_plural = 'ClientOrders'

    def __str__(self):
        return f'Order N-{self.id}'
