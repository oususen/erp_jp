from extensions.common.base import *
from extensions.models import *


class StockCheckOrder(Model):
    """棚卸伝票"""

    class Status(TextChoices):
        """棚卸状況"""

        SURPLUS = ('surplus', '棚卸超過')
        LOSS = ('loss', '棚卸不足')
        UNCHANGED = ('unchanged', '変化なし')

    number = CharField(max_length=32, verbose_name='番号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT,
                           related_name='stock_check_orders', verbose_name='倉庫')
    handler = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='stock_check_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理時間')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    status = CharField(max_length=32, choices=Status.choices, null=True, verbose_name='棚卸状況')
    total_book_quantity = FloatField(null=True, verbose_name='帳簿総数量')
    total_actual_quantity = FloatField(null=True, verbose_name='実総数量')
    total_surplus_quantity = FloatField(null=True, verbose_name='棚卸超過総数量')
    total_surplus_amount = AmountField(null=True, verbose_name='棚卸超過総金額')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_check_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_orders')

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
            number = 'PD' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class StockCheckGoods(Model):
    """棚卸商品"""

    class Status(TextChoices):
        """棚卸状況"""

        SURPLUS = ('surplus', '棚卸超過')
        LOSS = ('loss', '棚卸不足')
        UNCHANGED = ('unchanged', '変化なし')

    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE,
                                   related_name='stock_check_goods_set', verbose_name='棚卸伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_check_goods_set', verbose_name='製品')
    book_quantity = FloatField(verbose_name='帳簿数量')
    actual_quantity = FloatField(verbose_name='実数量')
    surplus_quantity = FloatField(verbose_name='棚卸超過数量')
    purchase_price = FloatField(verbose_name='購買単価')
    surplus_amount = AmountField(verbose_name='棚卸超過金額')
    status = CharField(max_length=32, choices=Status.choices, verbose_name='棚卸状況')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_goods_set')

    class Meta:
        unique_together = [('stock_check_order', 'goods')]


class StockCheckBatch(Model):
    """棚卸ロット"""

    class Status(TextChoices):
        """棚卸状況"""

        SURPLUS = ('surplus', '棚卸超過')
        LOSS = ('loss', '棚卸不足')
        UNCHANGED = ('unchanged', '変化なし')

    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE,
                                   related_name='stock_check_batchs', verbose_name='棚卸伝票')
    stock_check_goods = ForeignKey('stock_check.StockCheckGoods', on_delete=CASCADE,
                                   related_name='stock_check_batchs', verbose_name='棚卸商品')
    batch_number = CharField(max_length=32, verbose_name='ロットコード')
    production_date = DateField(null=True, verbose_name='製造日')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='stock_check_batchs', verbose_name='製品')
    book_quantity = FloatField(verbose_name='帳簿数量')
    actual_quantity = FloatField(verbose_name='実数量')
    surplus_quantity = FloatField(verbose_name='棚卸超過数量')
    status = CharField(max_length=32, choices=Status.choices, verbose_name='棚卸状況')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_check_batchs')

    class Meta:
        unique_together = [('stock_check_goods', 'batch_number')]


__all__ = [
    'StockCheckOrder', 'StockCheckGoods', 'StockCheckBatch',
]
