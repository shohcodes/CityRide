from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.orders.filters import DriverOrderFilter
from apps.orders.models import DriverOrders, ClientOrder
from apps.orders.permissions import DriverOrderPermission, ClientOrderPermission
from apps.orders.serializers import DriverOrdersSerializers, ClientOrdersSerializers, DriverOrdersCreateSerializer, \
    ClientOrdersCreateSerializers, DriverOrdersListSerializers, ClientOrdersAcceptSerializer, \
    DriverOrdersDetailSerializer, ClientOrdersListSerializer, ClientOrderDetailSerializer, \
    ClientOrderForDriverSerializer
from apps.users.choices import UsersRoleChoices


class DriverOrdersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                          mixins.DestroyModelMixin):
    queryset = DriverOrders.objects.all()
    serializer_class = DriverOrdersSerializers
    permission_classes = [IsAuthenticated, DriverOrderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DriverOrderFilter  # noqa

    def get_serializer_class(self):
        if self.action == 'create':
            return DriverOrdersCreateSerializer
        elif self.action == 'list':
            return DriverOrdersListSerializers
        elif self.action == 'retrieve':
            return DriverOrdersDetailSerializer
        return self.serializer_class


class ClientOrdersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet,
                          mixins.DestroyModelMixin):
    queryset = ClientOrder.objects.all()
    serializer_class = ClientOrdersSerializers
    permission_classes = [IsAuthenticated, ClientOrderPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientOrdersCreateSerializers
        elif self.action == 'list':
            return ClientOrdersListSerializer
        elif self.action == 'retrieve':
            return ClientOrderDetailSerializer
        elif self.action == 'by_driver_order':
            return ClientOrderForDriverSerializer
        return self.serializer_class

    @action(detail=True, methods=['GET'])
    def by_driver_order(self, request, pk=None):
        try:
            driver_order = DriverOrders.objects.get(pk=pk, driver=request.user)
        except DriverOrders.DoesNotExist:
            return Response({"error": "DriverOrder not found"}, status=404)

        client_orders = ClientOrder.objects.filter(driver_order=driver_order)
        serializer = self.get_serializer(client_orders, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.role == UsersRoleChoices.ADMIN:
            queryset = self.get_queryset()
        else:
            queryset = queryset.filter(Q(client=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        driver_order_id = request.data.get('driver_order')
        existing_order = ClientOrder.objects.filter(client=request.user, driver_order=driver_order_id).first()

        if existing_order:
            return Response({"error": "Client already has an order for this DriverOrder"},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class ClientOrderAcceptViewSet(UpdateAPIView):
    queryset = ClientOrder.objects.all()
    serializer_class = ClientOrdersAcceptSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT']
