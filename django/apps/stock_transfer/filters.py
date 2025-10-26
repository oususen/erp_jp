from django_filters.rest_framework import FilterSet
from django_filters.filters import *
from apps.stock_transfer.models import *


class StockTransferOrderFilter(FilterSet):
    start_date = DateFilter(field_name='create_time', lookup_expr='gte', label='開始日')
    end_date = DateFilter(field_name='create_time', lookup_expr='lt', label='終了日')

    class Meta:
        model = StockTransferOrder
        fields = ['number', 'out_warehouse', 'in_warehouse', 'handler', 'is_void', 'creator',
                  'start_date', 'end_date']


__all__ = [
    'StockTransferOrderFilter',
]
