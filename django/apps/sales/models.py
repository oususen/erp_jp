from extensions.common.base import *
from extensions.models import *


class SalesOrder(Model):
    """販売伝票"""

    number = CharField(max_length=32, verbose_name='番号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_orders', verbose_name='倉庫')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_orders', verbose_name='顧客')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理時間')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='販売総数量')
    discount = FloatField(default=1, verbose_name='全伝票割引')
    other_amount = AmountField(default=0, verbose_name='その他費用')
    total_amount = AmountField(null=True, verbose_name='販売総金額')
    collection_amount = AmountField(null=True, verbose_name='入金金額')
    arrears_amount = AmountField(null=True, verbose_name='借入金額')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='自動出庫有効化')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_orders')

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
            number = 'XS' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class SalesGoods(Model):
    """販売商品"""

    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE,
                             related_name='sales_goods_set', verbose_name='販売伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_goods_set', verbose_name='製品')
    sales_quantity = FloatField(verbose_name='販売数量')
    sales_price = FloatField(verbose_name='販売単価')
    total_amount = AmountField(verbose_name='総金額')
    return_quantity = FloatField(default=0, verbose_name='返品数量')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_goods_set')

    class Meta:
        unique_together = [('sales_order', 'goods')]


class SalesAccount(Model):
    """販売決済口座"""

    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE,
                             related_name='sales_accounts', verbose_name='販売伝票')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='sales_accounts', verbose_name='決済口座')
    collection_amount = AmountField(verbose_name='入金金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_accounts')

    class Meta:
        unique_together = [('sales_order', 'account')]


class SalesReturnOrder(Model):
    """販売返品伝票"""

    number = CharField(max_length=32, verbose_name='番号')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='sales_return_orders', verbose_name='販売伝票')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='倉庫')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='顧客')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='sales_return_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理時間')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='返品総数量')
    other_amount = AmountField(default=0, verbose_name='その他費用')
    total_amount = AmountField(null=True, verbose_name='返品総金額')
    payment_amount = AmountField(null=True, verbose_name='支払金額')
    arrears_amount = AmountField(null=True, verbose_name='借入金額')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='自動入庫有効化')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_sales_return_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_orders')

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
            number = 'SR' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class SalesReturnGoods(Model):
    """販売返品商品"""

    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE,
                                    related_name='sales_return_goods_set', verbose_name='販売返品伝票')
    sales_goods = ForeignKey('sales.SalesGoods', on_delete=CASCADE, null=True,
                             related_name='sales_return_goods_set', verbose_name='販売商品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='sales_return_goods_set', verbose_name='製品')
    return_quantity = FloatField(verbose_name='返品数量')
    return_price = FloatField(verbose_name='返品単価')
    total_amount = AmountField(verbose_name='総金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_goods_set')

    class Meta:
        unique_together = [('sales_return_order', 'goods')]


class SalesReturnAccount(Model):
    """販売返品決済口座"""

    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE,
                                    related_name='sales_return_accounts', verbose_name='販売返品伝票')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='sales_return_accounts', verbose_name='決済口座')
    payment_amount = AmountField(verbose_name='支払金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='sales_return_accounts')

    class Meta:
        unique_together = [('sales_return_order', 'account')]


__all__ = [
    'SalesOrder', 'SalesGoods', 'SalesAccount',
    'SalesReturnOrder', 'SalesReturnGoods', 'SalesReturnAccount',
]
