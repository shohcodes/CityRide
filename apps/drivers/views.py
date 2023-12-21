from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from apps.drivers.models import Drivers, CarModels
from apps.drivers.permissions import DriverPermission
from apps.drivers.serializers import DriversSerializers, CarModelsSerializers, DriverCreateSerializer, \
    DriverListSerializer, DriverDetailSerializer, DriverAcceptSerializer
from apps.users.choices import UsersRoleChoices


class DriversViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                     mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializers
    permission_classes = [IsAuthenticated(), DriverPermission()]
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return DriverCreateSerializer
        elif self.action == 'list':
            return DriverListSerializer
        elif self.action == 'retrieve':
            return DriverDetailSerializer
        elif self.action == 'update':
            return DriverAcceptSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return self.permission_classes

    def update(self, request, *args, **kwargs):
        if request.user.role == UsersRoleChoices.ADMIN:
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class CarModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                      mixins.DestroyModelMixin):
    queryset = CarModels.objects.all()
    serializer_class = CarModelsSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
