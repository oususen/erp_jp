from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.production.models import *
from apps.sales.models import *
from apps.goods.models import *


class ProductionOrderSerializer(BaseSerializer):
    """生产单据"""

    class SalesGoodsItemSerializer(ModelSerializer):
        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')

        class Meta:
            model = SalesGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'sales_quantity',
                      'sales_price', 'total_amount', 'return_quantity', 'unit_name']

    sales_order_number = CharField(source='sales_order.number', read_only=True, label='販売伝票番号')
    sales_goods_items = SalesGoodsItemSerializer(
        source='sales_order.sales_goods_set', many=True, read_only=True, label='販売商品Item')
    goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名')
    status_display = CharField(source='get_status_display', read_only=True, label='ステータス')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')

    class Meta:
        model = ProductionOrder
        read_only_fields = ['id', 'sales_order_number', 'sales_goods_items', 'remain_quantity', 'goods_number',
                            'goods_name', 'quantity_produced', 'remain_quantity', 'status', 'status_display',
                            'creator', 'creator_name', 'create_time']
        fields = ['number', 'is_related', 'sales_order', 'goods', 'total_quantity',
                  'start_time', 'end_time', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value

    def validate_sales_order(self, instance):
        instance = self.validate_foreign_key(SalesOrder, instance, message='販売伝票が存在しません')
        return instance

    def validate_goods(self, instance):
        instance = self.validate_foreign_key(Goods, instance, message='商品が存在しません')
        return instance

    def validate_total_quantity(self, value):
        if value <= 0:
            raise ValidationError('生産数量がゼロ以下です')
        return value

    def validate(self, attrs):
        if attrs['is_related'] and not attrs['sales_order']:
            raise ValidationError('販売伝票が関連付けられていません')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['quantity_produced'] = 0
        validated_data['creator'] = self.user
        return super().create(validated_data)

    def save(self, **kwargs):
        kwargs['remain_quantity'] = self.validated_data['total_quantity']
        return super().save(**kwargs)


class ProductionRecordSerializer(BaseSerializer):
    """生产记录"""

    production_order_number = CharField(source='production_order.number', read_only=True, label='生产单号')
    goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')

    class Meta:
        model = ProductionRecord
        read_only_fields = ['id', 'production_order_number', 'goods', 'goods_number', 'goods_name', 'creator',
                            'creator_name', 'create_time']
        fields = ['production_order', 'production_quantity', *read_only_fields]

    def validate_production_order(self, instance):
        instance = self.validate_foreign_key(ProductionOrder, instance, message='生产单不存在')
        if instance.status != ProductionOrder.Status.IN_PROGRESS:
            raise ValidationError(f'作業指示書{instance.number}{instance.get_status_display()}、作成できません')
        return instance

    def validate_production_quantity(self, value):
        if value <= 0:
            raise ValidationError('生産数量がゼロ以下です')
        return value

    def create(self, validated_data):
        validated_data['goods'] = validated_data['production_order'].goods
        validated_data['creator'] = self.user
        return super().create(validated_data)


__all__ = [
    'ProductionOrderSerializer', 'ProductionRecordSerializer',
]
