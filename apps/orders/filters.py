from django_filters import FilterSet, DateFilter, TimeFilter, DateFromToRangeFilter
from rest_framework.filters import BaseFilterBackend

from apps.orders.models import DriverOrders


class OrderFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        fromm = request.query_params.get('fromm')
        to = request.query_params.get('to')
        time = request.query_params.get('time')
        if fromm:
            queryset = queryset.filter(fromm=fromm)
        if to:
            queryset = queryset.filter(to=to)
        if time:
            queryset = queryset.filter(time=time)
        return queryset


# class Order1Filter(FilterSet):
#     # time__date = DateFilter(field_name='time', lookup_expr='date', label='Date (yyyy-mm-dd)')
#     # time__time = TimeFilter(field_name='time', lookup_expr='time', label='Time (hh:mm)')
#
#     class Meta:
#         model = DriverOrders
#         fields = {
#             'fromm': ['exact', 'contains'],
#             'to': ['exact', 'contains'],
#             # 'time__date': ['exact', 'gte', 'lte'],
#             # 'time__time': ['exact', 'gte', 'lte'],
#         }
#
#     # Define custom filters for 'time' field
#     time__date = DateFilter(field_name='time', lookup_expr='date', label='Date (yyyy-mm-dd)')
#     time__time = TimeFilter(field_name='time', lookup_expr='time', label='Time (hh:mm)')
