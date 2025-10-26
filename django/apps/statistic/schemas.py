from extensions.common.schema import *
from extensions.serializers import *


class PurchaseReportParameter(Serializer):
    start_date = DateField(required=True, label='開始日')
    end_date = DateField(required=True, label='終了日')
    category = IntegerField(required=False, label='商品カテゴリー')


class PurchaseReportStatisticResponse(Serializer):
    total_count = IntegerField(label='購買回数')
    total_quantity = FloatField(label='購買数量')
    total_amount = AmountField(label='購買金額')


class PurchaseReportGroupByGoodsResponse(Serializer):
    goods = IntegerField(label='商品ID')
    goods_number = CharField(label='商品コード')
    goods_name = CharField(label='商品名')
    goods_barcode = CharField(label='商品バーコード')
    goods_spec = CharField(label='商品規格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_purchase_quantity = FloatField(label='購買総数量')
    total_purchase_amount = AmountField(label='購買総金額')
    min_purchase_price = FloatField(label='最低購買価格')
    avg_purchase_price = FloatField(label='平均購買価格')
    max_purchase_price = FloatField(label='最高購買価格')


class SalesReportParameter(Serializer):
    start_date = DateField(required=True, label='開始日')
    end_date = DateField(required=True, label='終了日')
    category = IntegerField(required=False, label='商品カテゴリー')


class SalesReportStatisticResponse(Serializer):
    total_count = IntegerField(label='販売回数')
    total_quantity = FloatField(label='販売数量')
    total_amount = AmountField(label='販売金額')


class SalesReportGroupByGoodsResponse(Serializer):
    goods = IntegerField(label='商品ID')
    goods_number = CharField(label='商品コード')
    goods_name = CharField(label='商品名')
    goods_barcode = CharField(label='商品バーコード')
    goods_spec = CharField(label='商品規格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_sales_quantity = FloatField(label='販売総数量')
    total_sales_amount = AmountField(label='販売総金額')
    min_sales_price = FloatField(label='最低販売価格')
    avg_sales_price = FloatField(label='平均販売価格')
    max_sales_price = FloatField(label='最高販売価格')


class SalesHotGoodsParameter(Serializer):
    start_date = DateField(required=True, label='開始日')
    end_date = DateField(required=True, label='終了日')


class SalesHotGoodsResponse(Serializer):
    goods = IntegerField(label='商品ID')
    goods_number = CharField(label='商品コード')
    goods_name = CharField(label='商品名')
    goods_barcode = CharField(label='商品バーコード')
    goods_spec = CharField(label='商品規格')
    category_name = CharField(label='分类名称')
    unit_name = CharField(label='单位名称')
    total_sales_quantity = FloatField(label='販売総数量')


class SalesTrendParameter(Serializer):
    start_date = DateField(required=True, label='開始日')
    end_date = DateField(required=True, label='終了日')


class SalesTrendResponse(Serializer):
    warehouse = IntegerField(label='倉庫ID')
    warehouse_number = CharField(label='商品コード')
    warehouse_name = CharField(label='商品名')
    total_sales_amount = AmountField(label='販売総金額')
    date = DateField(label='日期')


class FinanceStatisticParameter(Serializer):
    start_date = DateField(required=True, label='開始日')
    end_date = DateField(required=True, label='終了日')


class FinanceStatisticResponse(Serializer):
    total_sales_amount = AmountField(label='販売金額')
    total_sales_reutrn_amount = AmountField(label='販売返品金額')
    total_purchase_amount = AmountField(label='購買金額')
    total_purchase_return_amount = AmountField(label='購買返品金額')
    total_income_amount = AmountField(label='收入金额')
    total_expenditure_amount = AmountField(label='支出金额')


class HomeViewResponse(Serializer):
    sales_count = IntegerField(label='販売件数')
    sales_amount = AmountField(label='販売額')
    purchase_count = IntegerField(label='購買件数')
    stock_in_task_count = IntegerField(label='待入库')
    stock_out_task_count = IntegerField(label='待出库')
    inventory_warning_count = IntegerField(label='库存预警')
    arrears_receivable_amount = AmountField(label='应收欠款')
    arrears_payable_amount = AmountField(label='应付欠款')


__all__ = [
    'PurchaseReportParameter', 'PurchaseReportStatisticResponse', 'PurchaseReportGroupByGoodsResponse',
    'SalesReportParameter', 'SalesReportStatisticResponse', 'SalesReportGroupByGoodsResponse',
    'SalesHotGoodsParameter', 'SalesHotGoodsResponse', 'SalesTrendParameter', 'SalesTrendResponse',
    'FinanceStatisticParameter', 'FinanceStatisticResponse', 'HomeViewResponse',
]
