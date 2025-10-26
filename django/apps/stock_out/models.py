from extensions.common.base import *
from extensions.models import *


class StockOutOrder(Model):
    """出库通知单据"""

    class Type(TextChoices):
        """出库类型"""

        SALES = ('sales', '販売')
        PURCHASE_RETURN = ('purchase', '購買返品')
        STOCK_TRANSFER = ('stock_transfer', '在庫振替')

    number = CharField(max_length=32, verbose_name='番号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_out_orders', verbose_name='倉庫')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='出庫タイプ')
    sales_order = OneToOneField('sales.SalesOrder', on_delete=CASCADE, null=True,
                                related_name='stock_out_order', verbose_name='販売伝票')
    purchase_return_order = OneToOneField('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                          related_name='stock_out_order', verbose_name='購買返品伝票')
    stock_transfer_order = OneToOneField('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                         related_name='stock_out_order', verbose_name='在庫振替伝票')
    total_quantity = FloatField(verbose_name='出庫総数')
    remain_quantity = FloatField(default=0, verbose_name='出庫残数量')
    is_completed = BooleanField(default=False, verbose_name='完了状態')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_out_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_out_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today(), pendulum.tomorrow()
        instance = cls.objects.filter(team=team, create_time__gte=start_date.format('YYYY-MM-DD HH:mm:ss'), create_time__lt=end_date.format('YYYY-MM-DD HH:mm:ss')).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'CK' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockOutGoods(Model):
    """出库产品"""

    stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE,
                                 related_name='stock_out_goods_set', verbose_name='出庫通知伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_out_goods_set', verbose_name='製品')
    stock_out_quantity = FloatField(verbose_name='出庫総数')
    remain_quantity = FloatField(default=0, verbose_name='出庫残数量')
    is_completed = BooleanField(default=False, verbose_name='完了状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_out_goods_set')

    class Meta:
        unique_together = [('stock_out_order', 'goods')]


class StockOutRecord(Model):
    """出库记录"""

    stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE,
                                 related_name='stock_out_records', verbose_name='出庫通知伝票')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_out_records', verbose_name='倉庫')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_out_records', verbose_name='经手人')
    handle_time = DateField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='出庫総数')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_out_records', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_out_records')


class StockOutRecordGoods(Model):
    """出库记录产品"""

    stock_out_record = ForeignKey('stock_out.StockOutRecord', on_delete=CASCADE,
                                  related_name='stock_out_record_goods_set', verbose_name='出庫記録')
    stock_out_goods = ForeignKey('stock_out.StockOutGoods', on_delete=CASCADE,
                                 related_name='stock_out_record_goods_set', verbose_name='出庫商品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_out_record_goods_set', verbose_name='製品')
    stock_out_quantity = FloatField(verbose_name='出库数量')
    batch = ForeignKey('goods.Batch', on_delete=CASCADE, null=True,
                       related_name='stock_out_record_goods_set', verbose_name='バッチ')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_out_record_goods_set')

    class Meta:
        unique_together = [('stock_out_record', 'goods')]


__all__ = [
    'StockOutOrder', 'StockOutGoods',
    'StockOutRecord', 'StockOutRecordGoods',
]
