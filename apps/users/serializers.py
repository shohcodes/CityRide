from random import randint

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response

from apps.drivers.models import Drivers
from apps.users.choices import UsersRoleChoices
from apps.users.exceptions import IncorrectActivationCodeException
from apps.users.models import User, SMS
from apps.users.services import send_sms, check_activation_code
from apps.users.validators import phone_validator, activation_code_validator


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'role', 'is_verified']


class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'role', 'is_verified', 'is_active', 'is_staff', 'is_superuser',
                  'created_at', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name',
            'phone_number'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password']

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        send_sms(phone_number)
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = UsersRoleChoices.CLIENT.value
        instance = User.objects.create(**validated_data)
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number']


class VerifyUsersSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(validators=[phone_validator])
    code = serializers.IntegerField(validators=[activation_code_validator], write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        code = attrs.get('code')
        if not check_activation_code(phone_number, code):
            raise IncorrectActivationCodeException
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(validators=[phone_validator])


class ConfirmResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(validators=[phone_validator])
    code = serializers.IntegerField(validators=[activation_code_validator], write_only=True)
    new_password = serializers.CharField(max_length=255)
