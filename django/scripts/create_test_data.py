from django.db import transaction
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *


def run(*args):
    team = Team.objects.all().first()
    with transaction.atomic():
        Account.objects.create(number='A001', name='デフォルト口座', team=team)
        Client.objects.create(number='C001', name='デフォルト顧客', team=team)
        Supplier.objects.create(number='S001', name='デフォルト仕入先', team=team)

        warehouse = Warehouse.objects.create(number='W001', name='デフォルト倉庫', team=team)
        goods = Goods.objects.create(number='G001', name='商品A', purchase_price=10, retail_price=20,
                                     level_price1=20, level_price2=20, level_price3=20, team=team)
        Inventory.objects.create(warehouse=warehouse, goods=goods, team=team)
