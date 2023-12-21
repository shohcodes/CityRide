from datetime import datetime, timedelta

from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend

from apps.orders.models import DriverOrders


class DriverOrderFilters(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        fromm = request.query_params.get('fromm')
        to = request.query_params.get('to')
        time = request.query_params.get('time')
        if fromm:
            queryset = queryset.filter(fromm=fromm)
        if to:
            queryset = queryset.filter(to=to)
        if time:
            time_datetime = datetime.strptime(time, "%d.%m.%Y")
            queryset = queryset.filter(
                time__day=time_datetime.day,
                time__month=time_datetime.month,
                time__year=time_datetime.year
            )
        return queryset


class DriverOrderFilter(filters.FilterSet):
    time = filters.CharFilter(method='filter_by_time')

    def filter_by_time(self, queryset, name, value):
        try:
            parsed_date = datetime.strptime(value, '%d.%m.%Y')
            start_date = parsed_date.replace(hour=0, minute=0, second=0)
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(time__gte=start_date, time__lt=end_date)
        except ValueError:
            pass

        return queryset

    class Meta:
        model = DriverOrders
        fields = ['fromm', 'to', 'time']
