from extensions.serializers import *


class InventoryWarningResponse(Serializer):
    goods = IntegerField(label='商品ID')
    goods_number = CharField(label='商品コード')
    goods_name = CharField(label='商品名')
    goods_barcode = CharField(label='商品バーコード')
    unit_name = CharField(label='単位名')
    inventory_upper = FloatField(label='库存上限')
    inventory_lower = FloatField(label='库存下限')
    total_quantity = FloatField(label='在庫数量')


__all__ = [
    'InventoryWarningResponse',
]
