from django.db.models import Q
from rest_framework import mixins
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.orders.filters import OrderFilter
# from apps.orders.filters import Order1Filter
from apps.orders.models import DriverOrders, ClientOrder
from apps.orders.permissions import DriverOrderPermission
from apps.orders.serializers import DriverOrdersSerializers, ClientOrdersSerializers, DriverOrdersCreateSerializer, \
    ClientOrdersCreateSerializers, DriverOrdersListSerializers, ClientOrdersAcceptSerializer
from apps.users.choices import UsersRoleChoices


class DriverOrdersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                          mixins.DestroyModelMixin):
    queryset = DriverOrders.objects.all()
    serializer_class = DriverOrdersSerializers
    # permission_classes = [IsAuthenticated, DriverOrderPermission]
    filter_backends = [OrderFilter]

    # filter_class = Order1Filter

    def get_serializer_class(self):
        if self.action == 'create':
            return DriverOrdersCreateSerializer
        elif self.action == 'list':
            return DriverOrdersListSerializers  # todo list action
        return self.serializer_class


class ClientOrdersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                          mixins.DestroyModelMixin):
    queryset = ClientOrder.objects.all()
    serializer_class = ClientOrdersSerializers
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientOrdersCreateSerializers
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.role == UsersRoleChoices.ADMIN:
            queryset = self.get_queryset()
        else:
            queryset = queryset.filter(Q(client=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClientOrderAcceptViewSet(UpdateAPIView):
    queryset = ClientOrder.objects.all()
    serializer_class = ClientOrdersAcceptSerializer
    permission_classes = [IsAuthenticated]
