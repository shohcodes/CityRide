from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.drivers.models import Drivers, CarModels
from apps.users.choices import UsersRoleChoices
from apps.users.models import User
from apps.users.serializers import UserListSerializer, UsersDetailSerializer
from apps.users.services import send_sms


class DriversSerializers(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'


class DriverListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Drivers
        fields = [
            'id',
            'car_model',
            'car_photo',
            'user',
        ]


class DriverCreateSerializer(serializers.ModelSerializer):
    car_model = serializers.IntegerField(write_only=True)
    car_photo = serializers.ImageField(write_only=True)
    car_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['car_model', 'car_photo', 'car_number', 'full_name', 'phone_number', 'password']

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        send_sms(phone_number)
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = UsersRoleChoices.DRIVER.value
        car_model = validated_data.pop('car_model')
        car_photo = validated_data.pop('car_photo')
        car_number = validated_data.pop('car_number')
        instance = User.objects.create(**validated_data)
        Drivers.objects.create(
            user=instance,
            car_model_id=car_model,
            car_photo=car_photo,
            car_number=car_number,
        )
        return instance


class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = ['car_number', 'car_photo']


class CarModelsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarModels
        fields = '__all__'


class DriversSerializer(serializers.ModelSerializer):
    car_model = serializers.CharField(source='car_model.model')
    car_name = serializers.CharField(source='car_model.name')

    class Meta:
        model = Drivers
        fields = ['car_model', 'car_name', 'car_number', 'car_photo']


class DriverDetailSerializer(serializers.ModelSerializer):
    user = UsersDetailSerializer()
    car_model = CarModelsSerializers()

    class Meta:
        model = Drivers
        fields = [
            'car_model',
            'car_number',
            'car_photo',
            'user'
        ]


class DriversSerializer1(serializers.ModelSerializer):
    car_name = serializers.CharField(source='car_model.name')

    class Meta:
        model = Drivers
        fields = ['car_name']


class DriverAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = ['is_accepted']
