from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import DriverOrders, ClientOrder


class DriverOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriverOrders
        fields = '__all__'


class DriverOrdersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverOrders
        fields = ['fromm', 'to', 'time', 'price', 'seats']

    def validate(self, attrs):
        user = self.context['request'].user
        if user.role != 'driver':
            raise ValidationError('You are not a driver')
        else:
            return attrs

    def create(self, validated_data):
        validated_data['driver'] = self.context['request'].user
        instance = DriverOrders.objects.create(**validated_data)
        return instance


class DriverOrdersListSerializers(serializers.ModelSerializer):  # todo list action
    class Meta:
        model = DriverOrders
        fields = '__all__'


class ClientOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = '__all__'


class ClientOrdersCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = ['driver_order', 'lat', 'lng']

    def validate(self, attrs):
        user = self.context['request'].user
        if user.role != 'client':
            raise ValidationError('You are not a client!')
        else:
            return attrs

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        instance = ClientOrder.objects.create(**validated_data)
        return instance


class ClientOrdersAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = ['is_accepted']

    def validate(self, attrs):
        driver_order = self.instance.driver_order
        if driver_order.client_driver_order.count() == driver_order.seats:
            raise ValidationError("There are no empty seats in your car!")
        return attrs

    # def update(self, instance, validated_data):
    #     driver_order = instance.driver_order
    #     driver_order.seats -= 1
    #     driver_order.save()
    #     return super().update(instance, validated_data)
