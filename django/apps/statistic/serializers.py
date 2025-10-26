from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *
from apps.sales.models import *
from apps.finance.models import *


class PurchaseReportDetialSerializer(BaseSerializer):
    """購買詳細"""

    goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
    goods_spec = CharField(source='goods.spec', read_only=True, label='商品規格')
    category_name = CharField(source='goods.category.name', read_only=True, label='カテゴリー名')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')
    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='購買伝票番号')
    warehouse_number = CharField(source='purchase_order.warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='purchase_order.warehouse.name', read_only=True, label='倉庫名')
    supplier_number = CharField(source='purchase_order.supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='purchase_order.supplier.name', read_only=True, label='仕入先名')
    creator_name = CharField(source='purchase_order.creator.name', read_only=True, label='作成者名')
    create_time = DateTimeField(source='purchase_order.create_time', read_only=True, label='作成日時')

    class Meta:
        model = PurchaseGoods
        fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'goods_spec',
                  'purchase_quantity', 'category_name', 'unit_name', 'purchase_price', 'total_amount',
                  'purchase_order', 'purchase_order_number', 'warehouse_number', 'warehouse_name',
                  'supplier_number', 'supplier_name', 'creator_name', 'create_time']


class SalesReportDetialSerializer(BaseSerializer):
    """販売詳細"""

    goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
    goods_name = CharField(source='goods.name', read_only=True, label='商品名')
    goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
    goods_spec = CharField(source='goods.spec', read_only=True, label='商品規格')
    category_name = CharField(source='goods.category.name', read_only=True, label='カテゴリー名')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')
    sales_order_number = CharField(source='sales_order.number', read_only=True, label='購買伝票番号')
    warehouse_number = CharField(source='sales_order.warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='sales_order.warehouse.name', read_only=True, label='倉庫名')
    client_number = CharField(source='sales_order.supplier.number', read_only=True, label='仕入先コード')
    client_name = CharField(source='sales_order.supplier.name', read_only=True, label='仕入先名')
    creator_name = CharField(source='sales_order.creator.name', read_only=True, label='作成者名')
    create_time = DateTimeField(source='sales_order.create_time', read_only=True, label='作成日時')

    class Meta:
        model = SalesGoods
        fields = ['id', 'goods', 'goods_number', 'goods_name', 'goods_barcode', 'goods_spec',
                  'sales_quantity', 'category_name', 'unit_name', 'sales_price', 'total_amount',
                  'sales_order', 'sales_order_number', 'warehouse_number', 'warehouse_name',
                  'client_number', 'client_name', 'creator_name', 'create_time']


class PaymentOrderDetialSerializer(BaseSerializer):
    """支払詳細"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')

    class Meta:
        model = PaymentOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'discount_amount',
                  'total_amount', 'create_time']


class CollectionOrderDetialSerializer(BaseSerializer):
    """入金伝票"""

    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')

    class Meta:
        model = CollectionOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'discount_amount',
                  'total_amount', 'create_time']


class IncomeChargeOrderDetialSerializer(BaseSerializer):
    """収入費用詳細"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')
    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')

    class Meta:
        model = ChargeOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'supplier',
                  'supplier_number', 'supplier_name', 'charge_item_name', 'total_amount',
                  'charge_amount', 'create_time']


class ExpenditureChargeOrderDetialSerializer(BaseSerializer):
    """支出費用詳細"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')
    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')

    class Meta:
        model = ChargeOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'supplier',
                  'supplier_number', 'supplier_name', 'charge_item_name', 'total_amount',
                  'charge_amount', 'create_time']


class PurchasePaymentDetialSerializer(BaseSerializer):
    """采购支払詳細"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'total_amount',
                  'payment_amount', 'create_time']


class PurchaseReturnCollectionDetialSerializer(BaseSerializer):
    """購買返品入金詳細"""

    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')

    class Meta:
        model = PurchaseReturnOrder
        fields = ['id', 'number', 'supplier', 'supplier_number', 'supplier_name', 'total_amount',
                  'collection_amount', 'create_time']


class SalesCollectionDetialSerializer(BaseSerializer):
    """販売入金詳細"""

    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')

    class Meta:
        model = SalesOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'total_amount',
                  'collection_amount', 'create_time']


class SalesReturnPaymentDetialSerializer(BaseSerializer):
    """销售退货支払詳細"""

    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')

    class Meta:
        model = SalesReturnOrder
        fields = ['id', 'number', 'client', 'client_number', 'client_name', 'total_amount',
                  'payment_amount', 'create_time']


__all__ = [
    'PurchaseReportDetialSerializer', 'SalesReportDetialSerializer',
    'PaymentOrderDetialSerializer', 'CollectionOrderDetialSerializer',
    'IncomeChargeOrderDetialSerializer', 'ExpenditureChargeOrderDetialSerializer',
    'PurchasePaymentDetialSerializer', 'PurchaseReturnCollectionDetialSerializer',
    'SalesCollectionDetialSerializer', 'SalesReturnPaymentDetialSerializer',
]
