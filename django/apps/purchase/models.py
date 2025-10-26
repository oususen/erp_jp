from extensions.common.base import *
from extensions.models import *


class PurchaseOrder(Model):
    """購買伝票"""

    number = CharField(max_length=32, verbose_name='番号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_orders', verbose_name='倉庫')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_orders', verbose_name='仕入先')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理日時')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='購買総数量')
    other_amount = AmountField(default=0, verbose_name='その他費用')
    total_amount = AmountField(null=True, verbose_name='購買総金額')
    payment_amount = AmountField(null=True, verbose_name='支払金額')
    arrears_amount = AmountField(null=True, verbose_name='未払金額')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='自動入庫を有効化')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today().to_date_string(), pendulum.tomorrow().to_date_string()
        instance = cls.objects.filter(team=team, create_time__gte=start_date, create_time__lt=end_date).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'CG' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class PurchaseGoods(Model):
    """購買商品"""

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE,
                                related_name='purchase_goods_set', verbose_name='購買伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='purchase_goods_set', verbose_name='製品')
    purchase_quantity = FloatField(verbose_name='購買数量')
    purchase_price = FloatField(verbose_name='購買単価')
    total_amount = AmountField(verbose_name='総金額')
    return_quantity = FloatField(default=0, verbose_name='返品数量')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_goods_set')

    class Meta:
        unique_together = [('purchase_order', 'goods')]


class PurchaseAccount(Model):
    """購買決済口座"""

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE,
                                related_name='purchase_accounts', verbose_name='購買伝票')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='purchase_accounts', verbose_name='決済口座')
    payment_amount = AmountField(verbose_name='支払金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_accounts')

    class Meta:
        unique_together = [('purchase_order', 'account')]


class PurchaseReturnOrder(Model):
    """購買返品伝票"""

    number = CharField(max_length=32, verbose_name='番号')
    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='purchase_return_orders', verbose_name='購買伝票')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='倉庫')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='仕入先')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='purchase_return_orders', verbose_name='担当者')
    handle_time = DateField(verbose_name='処理日時')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    total_quantity = FloatField(null=True, verbose_name='返品総数量')
    other_amount = AmountField(default=0, verbose_name='その他費用')
    total_amount = AmountField(null=True, verbose_name='返品総金額')
    collection_amount = AmountField(null=True, verbose_name='入金金額')
    arrears_amount = AmountField(null=True, verbose_name='未払金額')
    is_void = BooleanField(default=False, verbose_name='無効状態')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='自動出庫を有効化')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_purchase_return_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_orders')

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
            number = 'CR' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class PurchaseReturnGoods(Model):
    """購買返品商品"""

    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE,
                                       related_name='purchase_return_goods_set', verbose_name='購買返品伝票')
    purchase_goods = ForeignKey('purchase.PurchaseGoods', on_delete=CASCADE, null=True,
                                related_name='purchase_return_goods_set', verbose_name='購買商品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT,
                       related_name='purchase_return_goods_set', verbose_name='製品')
    return_quantity = FloatField(verbose_name='返品数量')
    return_price = FloatField(verbose_name='返品単価')
    total_amount = AmountField(verbose_name='総金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_goods_set')

    class Meta:
        unique_together = [('purchase_return_order', 'goods')]


class PurchaseReturnAccount(Model):
    """購買返品決済口座"""

    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE,
                                       related_name='purchase_return_accounts', verbose_name='購買返品伝票')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='purchase_return_accounts', verbose_name='決済口座')
    collection_amount = AmountField(verbose_name='入金金額')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='purchase_return_accounts')

    class Meta:
        unique_together = [('purchase_return_order', 'account')]


__all__ = [
    'PurchaseOrder', 'PurchaseGoods', 'PurchaseAccount',
    'PurchaseReturnOrder', 'PurchaseReturnGoods', 'PurchaseReturnAccount',
]
