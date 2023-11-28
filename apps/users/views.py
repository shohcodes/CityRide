from django.contrib.auth.hashers import make_password
from django.http import Http404
from rest_framework import mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.exceptions import IncorrectActivationCodeException
from apps.users.models import User
from apps.users.serializers import UsersSerializer, UserCreateSerializer, UsersDetailSerializer, VerifyUsersSerializer, \
    ResetPasswordSerializer, ConfirmResetPasswordSerializer
from apps.users.services import send_sms, check_activation_code


class UsersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                   mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UsersDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return self.permission_classes

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user != instance:
                return Response('You cannot delete someone else`s account!')
            self.perform_destroy(instance)
            return Response('Account deleted successfully!')
        except Http404:
            raise NotFound(detail="Invalid token", code="invalid_token")  # todo to ask


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    user_data = {
        'id': user.id,
        'full_name': user.full_name,
        'phone_number': user.phone_number,
    }

    return Response(user_data)


class VerifyUsersAPIView(GenericAPIView):
    serializer_class = VerifyUsersSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(phone_number=serializer.data['phone_number'])
        except User.DoesNotExist:
            return Response('User not found with this phone number')
        user.is_verified = True
        user.save()
        return Response({"message": "Your phone number has been confirmed"}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                User.objects.get(phone_number=phone_number)
                send_sms(phone_number)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this phone number"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Verification code sent to your phone number"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPasswordAPIView(CreateAPIView):
    serializer_class = ConfirmResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({"detail": "User not found with this phone number."},
                                status=status.HTTP_400_BAD_REQUEST)
            if check_activation_code(phone_number, code):
                user.password = make_password(new_password)
                user.save()
                return Response({"detail": "Password had reset successfully."}, status=status.HTTP_200_OK)
            else:
                raise IncorrectActivationCodeException
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
