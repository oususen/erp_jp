from apps.system.models import PermissionGroup, Permission


PERMISSIONS = [
    {
        'name': '首页',
        'permissions': [
            {'name': '販売推移', 'code': 'sales_trend'},
            {'name': '販売トップ10商品', 'code': 'sales_hot_goods'},
            {'name': '入库任务提醒', 'code': 'stock_in_reminder'},
            {'name': '出库任务提醒', 'code': 'stock_out_reminder'},
            {'name': '库存预警', 'code': 'inventory_warning'},
        ],
    },
    {
        'name': '报表统计',
        'permissions': [
            {'name': '販売レポート', 'code': 'sales_report'},
            {'name': '購買レポート', 'code': 'purchase_report'},
            {'name': '库存报表', 'code': 'inventory'},
            {'name': 'ロットレポート', 'code': 'batch'},
            {'name': '收支统计', 'code': 'finance_statistic'},
        ],
    },
    {
        'name': '基础数据',
        'permissions': [
            {'name': '顧客管理', 'code': 'client'},
            {'name': '仕入先管理', 'code': 'supplier'},
            {'name': '倉庫管理', 'code': 'warehouse'},
            {'name': '決済アカウント', 'code': 'account'},
            {'name': '收支项目', 'code': 'charge_item'},
        ],
    },
    {
        'name': '商品管理',
        'permissions': [
            {'name': '商品カテゴリー', 'code': 'goods_category'},
            {'name': '商品単位', 'code': 'goods_unit'},
            {'name': '商品情報', 'code': 'goods'},
        ],
    },
    {
        'name': '購買管理',
        'permissions': [
            {'name': '購買発行', 'code': 'purchase_order'},
            {'name': '購買返品', 'code': 'purchase_return_order'},
        ],
    },
    {
        'name': '販売管理',
        'permissions': [
            {'name': '販売発行', 'code': 'sales_order'},
            {'name': '販売返品', 'code': 'sales_return_order'},
        ],
    },
    {
        'name': '生产管理',
        'permissions': [
            {'name': '生产计划', 'code': 'production_order'},
            {'name': '生产记录', 'code': 'production_record'},
        ],
    },
    {
        'name': '库内管理',
        'permissions': [
            {'name': '入库', 'code': 'stock_in'},
            {'name': '出库', 'code': 'stock_out'},
            {'name': '棚卸', 'code': 'stock_check'},
            {'name': '在庫振替', 'code': 'stock_transfer'},
            {'name': '库存流水', 'code': 'inventory_flow'},
        ],
    },
    {
        'name': '财务管理',
        'permissions': [
            {'name': '应付欠款', 'code': 'supplier_arrears'},
            {'name': '支払', 'code': 'payment_order'},
            {'name': '应收欠款', 'code': 'client_arrears'},
            {'name': '入金', 'code': 'collection_order'},
            {'name': '口座振替', 'code': 'account_transfer_record'},
            {'name': '日常收支', 'code': 'charge_order'},
            {'name': '资金流水', 'code': 'finance_flow'},
        ],
    },
]


def run(*args):
    PermissionGroup.objects.all().delete()

    for permission_group_item in PERMISSIONS:
        permission_group = PermissionGroup.objects.create(name=permission_group_item['name'])
        Permission.objects.bulk_create([Permission(group=permission_group, name=item['name'], code=item['code'])
                                        for item in permission_group_item['permissions']])
