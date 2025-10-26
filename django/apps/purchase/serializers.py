from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.purchase.models import *
from apps.finance.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *


class PurchaseOrderSerializer(BaseSerializer):
    """購買伝票"""

    class PurchaseGoodsItemSerializer(BaseSerializer):
        """購買商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')

        class Meta:
            model = PurchaseGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'purchase_quantity', 'purchase_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品が存在しません')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]が有効化されていません')
            return instance

        def validate_purchase_quantity(self, value):
            if value <= 0:
                raise ValidationError('購買数量がゼロ以下です')
            return value

        def validate_purchase_price(self, value):
            if value <= 0:
                raise ValidationError('購買単価がゼロ以下です')
            return value

    class PurchaseAccountItemSerializer(BaseSerializer):
        """購買決済口座"""

        account_number = CharField(source='account.number', read_only=True, label='口座コード')
        account_name = CharField(source='account.name', read_only=True, label='口座名')

        class Meta:
            model = PurchaseAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'payment_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='口座が存在しません')
            if not instance.is_active:
                raise ValidationError(f'口座[{instance.name}]が有効化されていません')
            return instance

        def validate_payment_amount(self, value):
            if value <= 0:
                raise ValidationError('支払金額がゼロ以下です')
            return value

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')
    handler_name = CharField(source='handler.name', read_only=True, label='担当者名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    purchase_goods_items = PurchaseGoodsItemSerializer(
        source='purchase_goods_set', many=True, label='購買商品Item')
    purchase_account_items = PurchaseAccountItemSerializer(
        source='purchase_accounts', required=False, many=True, label='購買決済口座Item')

    class Meta:
        model = PurchaseOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'supplier_number',
                            'supplier_name', 'handler_name', 'total_quantity', 'total_amount',
                            'payment_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_in', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'supplier', 'handler', 'handle_time', 'remark', 'other_amount',
                  'purchase_goods_items', 'purchase_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'番号[{value}]は既に存在します')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='倉庫が存在しません')
        if not instance.is_active:
            raise ValidationError(f'倉庫[{instance.name}]が有効化されていません')

        return instance

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='仕入先が存在しません')
        if not instance.is_active:
            raise ValidationError(f'仕入先[{instance.name}]が有効化されていません')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='担当者が存在しません')
        if not instance.is_active:
            raise ValidationError(f'担当者[{instance.name}]が有効化されていません')
        return instance

    def validate_other_amount(self, value):
        if value < 0:
            raise ValidationError('その他費用がゼロ未満です')
        return value

    @transaction.atomic
    def create(self, validated_data):
        purchase_goods_items = validated_data.pop('purchase_goods_set')
        purchase_account_items = validated_data.pop('purchase_accounts', [])

        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        purchase_order = super().create(validated_data)

        total_purchase_quantity = 0
        total_purchase_amount = 0

        # 購買商品を作成
        purchase_goods_set = []
        for purchase_goods_item in purchase_goods_items:
            purchase_quantity = purchase_goods_item['purchase_quantity']
            purchase_price = purchase_goods_item['purchase_price']
            total_amount = NP.times(purchase_quantity, purchase_price)
            purchase_goods_set.append(PurchaseGoods(
                purchase_order=purchase_order, goods=purchase_goods_item['goods'],
                purchase_quantity=purchase_quantity, purchase_price=purchase_price,
                total_amount=total_amount, team=self.team
            ))

            total_purchase_quantity = NP.plus(total_purchase_quantity, purchase_quantity)
            total_purchase_amount = NP.plus(total_purchase_amount, total_amount)
        else:
            PurchaseGoods.objects.bulk_create(purchase_goods_set)
            total_purchase_amount = NP.plus(total_purchase_amount, purchase_order.other_amount)
            purchase_order.total_quantity = total_purchase_quantity
            purchase_order.total_amount = total_purchase_amount

        total_payment_amount = 0

        if purchase_account_items:
            # 購買決済口座を作成
            purchase_accounts = []
            for purchase_account_item in purchase_account_items:
                payment_amount = purchase_account_item['payment_amount']
                purchase_accounts.append(PurchaseAccount(
                    purchase_order=purchase_order, account=purchase_account_item['account'],
                    payment_amount=payment_amount, team=self.team
                ))

                total_payment_amount = NP.plus(total_payment_amount, payment_amount)
            else:
                PurchaseAccount.objects.bulk_create(purchase_accounts)

        purchase_order.payment_amount = total_payment_amount
        purchase_order.arrears_amount = NP.minus(total_purchase_amount, total_payment_amount)
        purchase_order.save(update_fields=['total_quantity', 'total_amount', 'payment_amount',
                                           'arrears_amount'])

        return purchase_order


class PurchaseReturnOrderSerializer(BaseSerializer):
    """購買返品伝票"""

    class PurchaseReturnGoodsItemSerializer(BaseSerializer):
        """購買返品商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')

        class Meta:
            model = PurchaseReturnGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode',
                                'total_amount', 'unit_name']
            fields = ['purchase_goods', 'goods', 'return_quantity', 'return_price', *read_only_fields]

        def validate_purchase_goods(self, instance):
            instance = self.validate_foreign_key(PurchaseGoods, instance, message='購買商品が存在しません')
            return instance

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品が存在しません')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]が有効化されていません')
            return instance

        def validate_return_quantity(self, value):
            if value <= 0:
                raise ValidationError('返品数量がゼロ以下です')
            return value

        def validate_return_price(self, value):
            if value <= 0:
                raise ValidationError('返品単価がゼロ以下です')
            return value

    class PurchaseReturnAccountItemSerializer(BaseSerializer):
        """購買返品決済口座"""

        account_number = CharField(source='account.number', read_only=True, label='口座コード')
        account_name = CharField(source='account.name', read_only=True, label='口座名')

        class Meta:
            model = PurchaseReturnAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'collection_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='口座が存在しません')
            if not instance.is_active:
                raise ValidationError(f'口座[{instance.name}]が有効化されていません')
            return instance

        def validate_collection_amount(self, value):
            if value <= 0:
                raise ValidationError('入金金額がゼロ以下です')
            return value

    purchase_order_number = CharField(source='purchase_order.number', read_only=True, label='購買伝票コード')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    supplier_number = CharField(source='supplier.number', read_only=True, label='仕入先コード')
    supplier_name = CharField(source='supplier.name', read_only=True, label='仕入先名')
    handler_name = CharField(source='handler.name', read_only=True, label='担当者名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    purchase_return_goods_items = PurchaseReturnGoodsItemSerializer(
        source='purchase_return_goods_set', many=True, label='購買返品商品Item')
    purchase_return_account_items = PurchaseReturnAccountItemSerializer(
        source='purchase_return_accounts', required=False, many=True, label='購買返品決済口座Item')

    class Meta:
        model = PurchaseReturnOrder
        read_only_fields = ['id', 'purchase_order_number', 'warehouse_number', 'warehouse_name',
                            'supplier_number', 'supplier_name', 'handler_name', 'total_quantity',
                            'total_amount', 'collection_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_out', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'purchase_order', 'warehouse', 'supplier', 'handler', 'handle_time',
                  'remark', 'other_amount', 'purchase_return_goods_items',
                  'purchase_return_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'番号[{value}]は既に存在します')
        return value

    def validate_purchase_order(self, instance):
        instance = self.validate_foreign_key(PurchaseOrder, instance, message='購買伝票が存在しません')
        if instance.is_void:
            raise ValidationError(f'購買伝票[{instance.name}]は無効化されています')
        return instance

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='倉庫が存在しません')
        if not instance.is_active:
            raise ValidationError(f'倉庫[{instance.name}]が有効化されていません')

        return instance

    def validate_supplier(self, instance):
        instance = self.validate_foreign_key(Supplier, instance, message='仕入先が存在しません')
        if not instance.is_active:
            raise ValidationError(f'仕入先[{instance.name}]が有効化されていません')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='担当者が存在しません')
        if not instance.is_active:
            raise ValidationError(f'担当者[{instance.name}]が有効化されていません')
        return instance

    def validate(self, attrs):
        if purchase_order := attrs.get('purchase_order'):
            if purchase_order.warehouse != attrs['warehouse']:
                raise ValidationError(f'購買伝票[{purchase_order.number}]の選択が間違っています')

            if purchase_order.supplier != attrs['supplier']:
                raise ValidationError(f'購買伝票[{purchase_order.number}]の選択が間違っています')

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        purchase_return_goods_items = validated_data.pop('purchase_return_goods_set')
        purchase_return_account_items = validated_data.pop('purchase_return_accounts', [])

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['creator'] = self.user
        purchase_return_order = super().create(validated_data)

        total_return_quantity = 0
        total_return_amount = 0

        # 購買返品商品を作成
        purchase_return_goods_set = []
        for purchase_return_goods_item in purchase_return_goods_items:
            goods = purchase_return_goods_item['goods']
            return_quantity = purchase_return_goods_item['return_quantity']

            purchase_goods = None
            if purchase_order := purchase_return_order.purchase_order:
                if not (purchase_goods := purchase_return_goods_item.get('purchase_goods')):
                    raise ValidationError(f'購買伝票[{purchase_order.number}]に商品[{goods.name}]が存在しません')

                purchase_goods.return_quantity = NP.plus(purchase_goods.return_quantity, return_quantity)
                if purchase_goods.return_quantity > purchase_goods.purchase_quantity:
                    raise ValidationError(f'返品商品[{goods.name}]の返品数量が間違っています')

                # 購買商品の返品数量を同期
                purchase_goods.save(update_fields=['return_quantity'])

            return_price = purchase_return_goods_item['return_price']
            total_amount = NP.times(return_quantity, return_price)
            purchase_return_goods_set.append(PurchaseReturnGoods(
                purchase_return_order=purchase_return_order, purchase_goods=purchase_goods,
                goods=goods, return_quantity=return_quantity, return_price=return_price,
                total_amount=total_amount, team=self.team
            ))

            total_return_quantity = NP.plus(total_return_quantity, return_quantity)
            total_return_amount = NP.plus(total_return_amount, total_amount)
        else:
            PurchaseReturnGoods.objects.bulk_create(purchase_return_goods_set)
            total_return_amount = NP.plus(total_return_amount, purchase_return_order.other_amount)
            purchase_return_order.total_quantity = total_return_quantity
            purchase_return_order.total_amount = total_return_amount

        total_collection_amount = 0

        if purchase_return_account_items:
            # 購買返品決済口座を作成
            purchase_return_accounts = []
            for purchase_return_account_item in purchase_return_account_items:
                collection_amount = purchase_return_account_item['collection_amount']
                purchase_return_accounts.append(PurchaseReturnAccount(
                    purchase_return_order=purchase_return_order,
                    account=purchase_return_account_item['account'],
                    collection_amount=collection_amount, team=self.team
                ))

                total_collection_amount = NP.plus(total_collection_amount, collection_amount)
            else:
                PurchaseReturnAccount.objects.bulk_create(purchase_return_accounts)

        purchase_return_order.collection_amount = total_collection_amount
        purchase_return_order.arrears_amount = NP.minus(total_return_amount, total_collection_amount)
        purchase_return_order.save(update_fields=['total_quantity', 'total_amount', 'collection_amount',
                                                  'arrears_amount'])

        return purchase_return_order


__all__ = [
    'PurchaseOrderSerializer', 'PurchaseReturnOrderSerializer',
]
