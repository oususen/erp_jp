from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.stock_out.models import *
from apps.goods.models import *
from apps.system.models import *


class StockOutOrderSerializer(BaseSerializer):
    """出库通知单据"""

    class StockOutGoodsItemSerializer(BaseSerializer):
        """出库产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')
        enable_batch_control = BooleanField(source='goods.enable_batch_control',
                                            read_only=True, label='ロット制御を有効化')

        class Meta:
            model = StockOutGoods
            fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'stock_out_quantity',
                      'remain_quantity', 'unit_name', 'enable_batch_control', 'is_completed']

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    type_display = CharField(source='get_type_display', read_only=True, label='出庫タイプ')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='販売伝票番号')
    purchase_return_order_number = CharField(source='purchase_return_order.number',
                                             read_only=True, label='購買返品伝票番号')
    stock_transfer_order_number = CharField(source='stock_transfer_order.number',
                                            read_only=True, label='在庫振替伝票番号')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    stock_out_goods_items = StockOutGoodsItemSerializer(
        source='stock_out_goods_set', many=True, label='出庫商品')

    class Meta:
        model = StockOutOrder
        fields = ['id', 'number', 'warehouse', 'warehouse_number', 'warehouse_name', 'type',
                  'type_display', 'sales_order', 'sales_order_number', 'purchase_return_order',
                  'purchase_return_order_number', 'stock_transfer_order', 'stock_transfer_order_number',
                  'total_quantity', 'remain_quantity', 'is_completed', 'is_void', 'creator',
                  'creator_name', 'create_time', 'stock_out_goods_items']


class StockOutRecordSerializer(BaseSerializer):
    """出庫記録"""

    class StockOutRecordGoodsSerializer(BaseSerializer):
        """出库记录产品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')
        enable_batch_control = BooleanField(source='goods.enable_batch_control',
                                            read_only=True, label='ロット制御を有効化')
        batch_number = CharField(source='batch.number', read_only=True, label='ロットコード')

        class Meta:
            model = StockOutRecordGoods
            read_only_fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'unit_name',
                                'enable_batch_control', 'batch_number']
            fields = ['stock_out_goods', 'stock_out_quantity', 'batch', *read_only_fields]

        def validate_stock_out_goods(self, instance):
            instance = self.validate_foreign_key(StockOutGoods, instance, message='出庫商品が存在しません')
            if instance.is_completed:
                raise ValidationError(f'出庫商品[{instance.goods.name}]已完成')
            return instance

        def validate_stock_out_quantity(self, value):
            if value <= 0:
                raise ValidationError('出庫数量がゼロ以下です')
            return value

        def validate_batch(self, instance):
            instance = self.validate_foreign_key(Batch, instance, message='ロットが存在しません')
            if instance and not instance.has_stock:
                raise ValidationError(f'ロット[{instance.number}]库存不足')
            return instance

        def validate(self, attrs):
            stock_out_goods = attrs['stock_out_goods']

            goods = stock_out_goods.goods

            if stock_out_goods.remain_quantity < attrs['stock_out_quantity']:
                raise ValidationError(f'商品[{goods.name}]の出庫数量が間違っています')

            if goods.enable_batch_control:
                if not (batch := attrs.get('batch')):
                    raise ValidationError(f'商品[{goods.name}]のロットが選択されていません')

                if batch.goods != attrs['stock_out_goods'].goods:
                    raise ValidationError(f'ロット[{batch.number}]の選択が間違っています')

                if batch.remain_quantity < attrs['stock_out_quantity']:
                    raise ValidationError(f'ロット[{batch.number}]库存不足')

            return super().validate(attrs)

    stock_out_order_number = CharField(source='stock_out_order.number', read_only=True, label='出庫通知伝票番号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    handler_name = CharField(source='handler.name', read_only=True, label='担当者名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    stock_out_record_goods_items = StockOutRecordGoodsSerializer(source='stock_out_record_goods_set',
                                                                 many=True, label='出庫記録商品')

    class Meta:
        model = StockOutRecord
        read_only_fields = ['id', 'stock_out_order_number', 'warehouse', 'warehouse_number',
                            'warehouse_name', 'handler_name', 'total_quantity', 'is_void', 'creator',
                            'creator_name', 'create_time']
        fields = ['stock_out_order', 'handler', 'handle_time', 'remark', 'stock_out_record_goods_items',
                  *read_only_fields]

    def validate_stock_out_order(self, instance):
        instance = self.validate_foreign_key(StockOutOrder, instance, message='出庫通知伝票が存在しません')
        if instance.is_void:
            raise ValidationError(f'出庫通知伝票[{instance.number}]已作废')

        if instance.is_completed:
            raise ValidationError(f'出庫通知伝票[{instance.number}]已完成')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='担当者が存在しません')
        if not instance.is_active:
            raise ValidationError(f'经手人[{instance.name}]未激活')
        return instance

    @transaction.atomic
    def create(self, validated_data):
        stock_out_record_goods_items = validated_data.pop('stock_out_record_goods_set')

        stock_out_order = validated_data['stock_out_order']
        validated_data['warehouse'] = stock_out_order.warehouse
        validated_data['creator'] = self.user
        stock_out_record = super().create(validated_data)

        total_stock_out_quantity = 0

        # 创建出库记录产品
        stock_out_record_goods_set = []
        for stock_out_record_goods_item in stock_out_record_goods_items:
            stock_out_goods = stock_out_record_goods_item['stock_out_goods']
            if stock_out_goods.stock_out_order != stock_out_order:
                raise ValidationError('出庫商品エラー')

            stock_out_quantity = stock_out_record_goods_item['stock_out_quantity']
            batch = stock_out_record_goods_item.get('batch')
            goods = stock_out_goods.goods

            stock_out_record_goods_set.append(StockOutRecordGoods(
                stock_out_record=stock_out_record, stock_out_goods=stock_out_goods, goods=goods,
                stock_out_quantity=stock_out_quantity, batch=batch, team=self.team
            ))

            total_stock_out_quantity = NP.plus(total_stock_out_quantity, stock_out_quantity)
        else:
            StockOutRecordGoods.objects.bulk_create(stock_out_record_goods_set)
            stock_out_record.total_quantity = total_stock_out_quantity
            stock_out_record.save(update_fields=['total_quantity'])

        return stock_out_record


__all__ = [
    'StockOutOrderSerializer', 'StockOutRecordSerializer',
]
