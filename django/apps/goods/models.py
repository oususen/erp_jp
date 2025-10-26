from extensions.common.base import *
from extensions.models import *


class GoodsCategory(Model):
    """商品カテゴリ"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_categories')

    class Meta:
        unique_together = [('name', 'team')]


class GoodsUnit(Model):
    """商品単位"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_units')

    class Meta:
        unique_together = [('name', 'team')]


class Goods(Model):
    """商品"""

    number = CharField(max_length=32, verbose_name='番号')
    name = CharField(max_length=64, verbose_name='名称')
    barcode = CharField(max_length=32, null=True, blank=True, verbose_name='バーコード')
    category = ForeignKey('goods.GoodsCategory', on_delete=SET_NULL, null=True,
                          related_name='goods_set', verbose_name='商品カテゴリ')
    unit = ForeignKey('goods.GoodsUnit', on_delete=SET_NULL, null=True,
                      related_name='goods_set', verbose_name='商品単位')
    spec = CharField(max_length=64, null=True, blank=True, verbose_name='仕様')
    enable_batch_control = BooleanField(default=False, verbose_name='ロット制御を有効化')
    shelf_life_days = IntegerField(null=True, verbose_name='品質保証期間日数')
    shelf_life_warning_days = IntegerField(default=0, verbose_name='期限切れ間近警告日')
    enable_inventory_warning = BooleanField(default=False, verbose_name='在庫警告を有効化')
    inventory_upper = FloatField(null=True, verbose_name='在庫上限')
    inventory_lower = FloatField(null=True, verbose_name='在庫下限')
    purchase_price = FloatField(default=0, verbose_name='購買価格')
    retail_price = FloatField(default=0, verbose_name='小売価格')
    level_price1 = FloatField(default=0, verbose_name='等級価格1')
    level_price2 = FloatField(default=0, verbose_name='等級価格2')
    level_price3 = FloatField(default=0, verbose_name='等級価格3')

    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    is_active = BooleanField(default=True, verbose_name='有効状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_set')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'G000000000001'
        if instance := cls.objects.filter(team=team).last():
            if result := re.findall('[0-9]+', instance.number):
                current_number = result[-1]
                next_number = str(int(current_number) + 1)

                if len(current_number) > len(next_number):
                    next_number = next_number.zfill(len(current_number))
            else:
                return default_number
        else:
            return default_number
        
        result = re.match(f'^(.*){current_number}(.*?)$', instance.number)
        prefix, suffix = result.group(1), result.group(2)

        return prefix + next_number + suffix


class GoodsImage(Model):
    """商品画像"""

    goods = ForeignKey('goods.Goods', on_delete=SET_NULL, null=True,
                       related_name='goods_images', verbose_name='商品')
    file = ImageField(verbose_name='ファイル')
    name = CharField(max_length=256, verbose_name='ファイル名')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='goods_images')


class Batch(Model):
    """ロット"""

    number = CharField(max_length=32, verbose_name='番号')
    inventory = ForeignKey('goods.Inventory', on_delete=CASCADE, related_name='batchs', verbose_name='在庫')
    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='batchs', verbose_name='入庫')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='batchs', verbose_name='商品')
    initial_quantity = FloatField(default=0, verbose_name='初期在庫')
    total_quantity = FloatField(verbose_name='ロット数量')
    remain_quantity = FloatField(verbose_name='ロットの残数量')
    production_date = DateField(null=True, verbose_name='製造日')
    shelf_life_days = IntegerField(null=True, verbose_name='品質保証期間日数')
    warning_date = DateField(null=True, verbose_name='警告日')
    expiration_date = DateField(null=True, verbose_name='期限切れ日')
    has_stock = BooleanField(default=True, verbose_name='在庫状態')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='batchs')

    class Meta:
        unique_together = [('number', 'warehouse', 'goods', 'team')]


class Inventory(Model):
    """在庫"""

    warehouse = ForeignKey('data.Warehouse', on_delete=CASCADE, related_name='inventories', verbose_name='入庫')
    goods = ForeignKey('goods.Goods', on_delete=CASCADE, related_name='inventories', verbose_name='商品')
    initial_quantity = FloatField(default=0, verbose_name='初期在庫')
    total_quantity = FloatField(default=0, verbose_name='在庫総数')
    has_stock = BooleanField(default=False, verbose_name='在庫状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventories')

    class Meta:
        unique_together = [('warehouse', 'goods', 'team')]


__all__ = [
    'GoodsCategory', 'GoodsUnit', 'Goods', 'GoodsImage',
    'Batch', 'Inventory',
]
