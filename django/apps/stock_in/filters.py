from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.stock_in.models import *


class StockInOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='開始日')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='終了日')

    class Meta:
        model = StockInOrder
        fields = ['number', 'warehouse', 'type', 'is_completed', 'is_void', 'creator',
                  'start_date', 'end_date']


class StockInRecordFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='開始日')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='終了日')

    class Meta:
        model = StockInRecord
        fields = ['stock_in_order', 'warehouse', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


__all__ = [
    'StockInOrderFilter', 'StockInRecordFilter',
]
