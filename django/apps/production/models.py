from extensions.common.base import *
from extensions.models import *


class ProductionOrder(Model):
    """生产单据"""

    class Status(TextChoices):
        IN_PLAN = ('in_plan', '計画中')
        IN_PROGRESS = ('in_progress', '進行中')
        COMPLETED = ('completed', '完了')
        CLOSED = ('closed', '強制終了')

    number = CharField(max_length=32, verbose_name='番号')
    is_related = BooleanField(default=False, verbose_name='関連状態')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=PROTECT, null=True, related_name='production_orders', verbose_name='販売伝票')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='production_orders', verbose_name='製品')
    total_quantity = FloatField(verbose_name='生産総数')
    quantity_produced = FloatField(verbose_name='生産済数量')
    remain_quantity = FloatField(verbose_name='残数量')
    start_time = DateTimeField(null=True, verbose_name='開始時間')
    end_time = DateTimeField(null=True, verbose_name='終了時間')
    status = CharField(max_length=32, choices=Status.choices, default=Status.IN_PLAN, verbose_name='ステータス')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_production_orders', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='production_orders')

    @classmethod
    def get_number(cls, team):
        start_date, end_date = pendulum.today().to_datetime_string(), pendulum.tomorrow().to_datetime_string()
        instance = cls.objects.filter(team=team, create_time__gte=start_date, create_time__lt=end_date).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'SC' + pendulum.today().format('YYYYMMDD') + '0001'

        return number


class ProductionRecord(Model):
    """生产记录"""

    production_order = ForeignKey('production.ProductionOrder', on_delete=CASCADE, related_name='production_records', verbose_name='生产单')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='production_records', verbose_name='製品')
    production_quantity = FloatField(verbose_name='生产数量')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_production_records', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='production_records')


__all__ = [
    'ProductionOrder', 'ProductionRecord',
]
