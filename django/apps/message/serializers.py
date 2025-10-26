from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_in.models import *
from apps.stock_out.models import *


class StockInOrderReminderSerializer(BaseSerializer):
    """入庫タスク通知"""

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')

    class Meta:
        model = StockInOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name',
                  'total_quantity', 'remain_quantity']


class StockOutOrderReminderSerializer(BaseSerializer):
    """出庫タスク通知"""

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')

    class Meta:
        model = StockOutOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name',
                  'total_quantity', 'remain_quantity']


__all__ = [
    'StockInOrderReminderSerializer', 'StockOutOrderReminderSerializer',
]
