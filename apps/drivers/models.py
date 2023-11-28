from django.db import models

from apps.core.models import TimeStampedModel
from apps.users.models import User


class CarModels(TimeStampedModel):
    model = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'

    def __str__(self):
        return f'{self.model}-{self.name}'


class Drivers(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModels, related_name='cars_models', on_delete=models.PROTECT)
    car_number = models.CharField(max_length=8)
    car_photo = models.ImageField(upload_to='cars_photos/')
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f'{self.car_model}-{self.car_number[3:6]}'
