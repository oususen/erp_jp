from extensions.common.base import *
from extensions.models import *


class StockTransferOrder(Model):
    """调拨单据"""

    number = CharField(max_length=32, verbose_name='番号')
    out_warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                                        related_name='out_stock_transfer_orders', verbose_name='出庫倉庫')
    in_warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                                       related_name='in_stock_transfer_orders', verbose_name='入庫倉庫')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_transfer_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理時間')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='振替総数量')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='自動出庫を有効化')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='自動入庫を有効化')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_transfer_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_transfer_orders')

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
            number = 'DB' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockTransferGoods(Model):
    """调拨产品"""

    stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE,
                                      related_name='stock_transfer_goods_set', verbose_name='在庫振替伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_transfer_goods_set', verbose_name='製品')
    stock_transfer_quantity = FloatField(verbose_name='振替数量')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_transfer_goods_set')

    class Meta:
        unique_together = [('stock_transfer_order', 'goods')]


__all__ = [
    'StockTransferOrder', 'StockTransferGoods',
]
