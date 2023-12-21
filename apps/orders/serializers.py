from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.drivers.serializers import DriversSerializer, DriversSerializer1
from apps.orders.models import DriverOrders, ClientOrder
from apps.users.serializers import UserNameSerializer, UsersDetailOrderSerializer, UserListSerializer, \
    UsersDetailSerializer


class DriverOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriverOrders
        fields = '__all__'


class DriverOrdersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverOrders
        fields = ['fromm', 'to', 'time', 'price', 'seats']

    def create(self, validated_data):
        last_order = DriverOrders.objects.filter(driver=self.context['request'].user).order_by('-time').first()
        if last_order and (timezone.now() - last_order.time) < timedelta(hours=24):
            raise serializers.ValidationError("You can only create an order every 24 hours.")

        validated_data['driver'] = self.context['request'].user
        instance = DriverOrders.objects.create(**validated_data)
        return instance


class DriverOrdersListSerializers(serializers.ModelSerializer):
    user = UserNameSerializer(source='driver', read_only=True)
    driver_details = DriversSerializer(source='driver.drivers', read_only=True)  # todo to ask
    time = serializers.DateTimeField(format="%d.%m.%Y-%H:%M:%S")

    class Meta:
        model = DriverOrders
        fields = ['id', 'user', 'driver_details', 'time']


class ClientOrderDriverOrdersSerializers(serializers.ModelSerializer):
    user = UserNameSerializer(source='driver', read_only=True)
    driver_details = DriversSerializer1(source='driver.drivers', read_only=True)
    time = serializers.DateTimeField(format="%d.%m.%Y-%H:%M:%S")

    class Meta:
        model = DriverOrders
        fields = ['id', 'fromm', 'to', 'user', 'driver_details', 'time']


class DriverOrdersDetailSerializer(serializers.ModelSerializer):
    user = UsersDetailOrderSerializer(source='driver', read_only=True)
    driver_details = DriversSerializer(source='driver.drivers', read_only=True)
    time = serializers.DateTimeField(format="%d.%m.%Y-%H:%M:%S")

    class Meta:
        model = DriverOrders
        fields = ['id', 'fromm', 'to', 'time', 'price', 'user', 'driver_details']


class ClientOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = '__all__'


class ClientOrdersCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = ['driver_order', 'lat', 'lng']

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        instance = ClientOrder.objects.create(**validated_data)
        return instance


class ClientOrdersListSerializer(serializers.ModelSerializer):
    client = UserListSerializer()
    driver_order = ClientOrderDriverOrdersSerializers()
    google_maps_ulr = serializers.SerializerMethodField('get_google_maps_ulr')
    yandex_maps_ulr = serializers.SerializerMethodField('get_yandex_maps_url')

    class Meta:
        model = ClientOrder
        fields = ['id', 'lat', 'lng', 'google_maps_ulr', 'yandex_maps_ulr', 'client', 'driver_order', 'is_accepted']

    def get_google_maps_ulr(self, obj):
        return f'https://www.google.com/maps?q={obj.lat},{obj.lng}'

    def get_yandex_maps_url(self, obj):
        return f'https://yandex.com/maps/?pt={obj.lng},{obj.lat}&z=12&l=map'


class ClientOrderDetailSerializer(serializers.ModelSerializer):
    client = UserListSerializer()
    driver_order = DriverOrdersDetailSerializer()
    google_maps_ulr = serializers.SerializerMethodField('get_google_maps_ulr')
    yandex_maps_ulr = serializers.SerializerMethodField('get_yandex_maps_url')

    class Meta:
        model = ClientOrder
        fields = ['id', 'lat', 'lng', 'google_maps_ulr', 'yandex_maps_ulr', 'client', 'driver_order', 'is_accepted']

    def get_google_maps_ulr(self, obj):
        return f'https://www.google.com/maps?q={obj.lat},{obj.lng}'

    def get_yandex_maps_url(self, obj):
        return f'https://yandex.com/maps/?pt={obj.lng},{obj.lat}&z=12&l=map'


class ClientOrderForDriverSerializer(serializers.ModelSerializer):
    client = UserListSerializer()
    google_maps_ulr = serializers.SerializerMethodField('get_google_maps_ulr')
    yandex_maps_ulr = serializers.SerializerMethodField('get_yandex_maps_url')

    class Meta:
        model = ClientOrder
        fields = ['id', 'lat', 'lng', 'google_maps_ulr', 'yandex_maps_ulr', 'client']

    def get_google_maps_ulr(self, obj):
        return f'https://www.google.com/maps?q={obj.lat},{obj.lng}'

    def get_yandex_maps_url(self, obj):
        return f'https://yandex.com/maps/?pt={obj.lng},{obj.lat}&z=12&l=map'


class ClientOrdersAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOrder
        fields = ['is_accepted']

    def validate(self, attrs):
        driver_order = self.instance.driver_order
        if driver_order.client_driver_order.count() == driver_order.seats:
            raise ValidationError("There are no empty seats in your car!")
        return attrs
