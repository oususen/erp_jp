from extensions.common.base import *
from extensions.models import *


class StockInOrder(Model):
    """入庫通知伝票"""

    class Type(TextChoices):
        """入庫タイプ"""

        PURCHASE = ('purchase', '購買')
        SALES_RETURN = ('sales_return', '販売返品')
        STOCK_TRANSFER = ('stock_transfer', '在庫振替')

    number = CharField(max_length=32, verbose_name='番号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_in_orders', verbose_name='倉庫')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='入庫タイプ')
    purchase_order = OneToOneField('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                   related_name='stock_in_order', verbose_name='購買伝票')
    sales_return_order = OneToOneField('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='stock_in_order', verbose_name='販売返品伝票')
    stock_transfer_order = OneToOneField('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                         related_name='stock_in_order', verbose_name='在庫振替伝票')
    total_quantity = FloatField(verbose_name='入庫総数')
    remain_quantity = FloatField(default=0, verbose_name='入庫残数量')
    is_completed = BooleanField(default=False, verbose_name='入庫完了状態')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today(), pendulum.tomorrow()
        instance = cls.objects.filter(create_time__gte=start_date.format('YYYY-MM-DD HH:mm:ss'),
                                      create_time__lt=end_date.format('YYYY-MM-DD HH:mm:ss'), team=team).last()
        print(instance)

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'RK' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockInGoods(Model):
    """入庫商品"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_goods_set', verbose_name='入庫通知伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_in_goods_set', verbose_name='製品')
    stock_in_quantity = FloatField(verbose_name='入庫総数')
    remain_quantity = FloatField(default=0, verbose_name='入庫残数量')
    is_completed = BooleanField(default=False, verbose_name='完了状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_goods_set')

    class Meta:
        unique_together = [('stock_in_order', 'goods')]


class StockInRecord(Model):
    """入庫記録"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_records', verbose_name='入庫通知伝票')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_in_records', verbose_name='倉庫')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_in_records', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理時間')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='入庫総数')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_records', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_records')


class StockInRecordGoods(Model):
    """入庫記録商品"""

    stock_in_record = ForeignKey('stock_in.StockInRecord', on_delete=CASCADE,
                                 related_name='stock_in_record_goods_set', verbose_name='入庫記録')
    stock_in_goods = ForeignKey('stock_in.StockInGoods', on_delete=CASCADE,
                                related_name='stock_in_record_goods_set', verbose_name='入庫商品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_in_record_goods_set', verbose_name='製品')
    stock_in_quantity = FloatField(verbose_name='入庫数量')
    batch = ForeignKey('goods.Batch', on_delete=CASCADE, null=True,
                       related_name='stock_in_record_goods_set', verbose_name='バッチ')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_record_goods_set')

    class Meta:
        unique_together = [('stock_in_record', 'goods')]


__all__ = [
    'StockInOrder', 'StockInGoods',
    'StockInRecord', 'StockInRecordGoods',
]
