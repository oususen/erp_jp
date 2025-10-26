from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.sales.models import *
from apps.data.models import *
from apps.goods.models import *
from apps.system.models import *
from apps.finance.models import *


class SalesOrderSerializer(BaseSerializer):
    """販売伝票"""

    class SalesGoodsItemSerializer(BaseSerializer):
        """販売商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')

        class Meta:
            model = SalesGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode', 'total_amount',
                                'return_quantity', 'unit_name']
            fields = ['goods', 'sales_quantity', 'sales_price', *read_only_fields]

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品が存在しません')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]は有効化されていません')
            return instance

        def validate_sales_quantity(self, value):
            if value <= 0:
                raise ValidationError('販売数量がゼロ以下です')
            return value

        def validate_sales_price(self, value):
            if value <= 0:
                raise ValidationError('販売単価がゼロ以下です')
            return value

    class SalesAccountItemSerializer(BaseSerializer):
        """販売決済口座"""

        account_number = CharField(source='account.number', read_only=True, label='口座コード')
        account_name = CharField(source='account.name', read_only=True, label='口座名')

        class Meta:
            model = SalesAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'collection_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='口座が存在しません')
            if not instance.is_active:
                raise ValidationError(f'口座[{instance.name}]は有効化されていません')
            return instance

        def validate_collection_amount(self, value):
            if value <= 0:
                raise ValidationError('入金金額がゼロ以下です')
            return value

    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')
    handler_name = CharField(source='handler.name', read_only=True, label='担当者名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    sales_goods_items = SalesGoodsItemSerializer(
        source='sales_goods_set', many=True, label='販売商品Item')
    sales_account_items = SalesAccountItemSerializer(
        source='sales_accounts', required=False, many=True, label='販売決済口座Item')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'warehouse_number', 'warehouse_name', 'client_number', 'client_name',
                            'handler_name', 'total_quantity', 'total_amount', 'collection_amount',
                            'arrears_amount', 'is_void', 'enable_auto_stock_out', 'creator',
                            'creator_name', 'create_time']
        fields = ['number', 'warehouse', 'client', 'handler', 'handle_time', 'discount', 'other_amount',
                  'remark', 'sales_goods_items', 'sales_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'番号[{value}]は既に存在します')
        return value

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='倉庫が存在しません')
        if not instance.is_active:
            raise ValidationError(f'倉庫[{instance.name}]は有効化されていません')

        return instance

    def validate_client(self, instance):
        instance = self.validate_foreign_key(Client, instance, message='顧客が存在しません')
        if not instance.is_active:
            raise ValidationError(f'顧客[{instance.name}]は有効化されていません')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='担当者が存在しません')
        if not instance.is_active:
            raise ValidationError(f'担当者[{instance.name}]は有効化されていません')
        return instance

    def validate_discount(self, value):
        if value <= 0:
            raise ValidationError('全伝票割引がゼロ以下です')
        return value

    def validate_other_amount(self, value):
        if value < 0:
            raise ValidationError('その他費用がゼロ未満です')
        return value

    @transaction.atomic
    def create(self, validated_data):
        sales_goods_items = validated_data.pop('sales_goods_set')
        sales_account_items = validated_data.pop('sales_accounts', [])

        validated_data['enable_auto_stock_out'] = self.team.enable_auto_stock_out
        validated_data['creator'] = self.user
        sales_order = super().create(validated_data)

        total_sales_quantity = 0
        total_sales_amount = 0

        # 販売商品を作成
        sales_goods_set = []
        for sales_goods_item in sales_goods_items:
            sales_quantity = sales_goods_item['sales_quantity']
            sales_price = sales_goods_item['sales_price']
            total_amount = NP.times(sales_quantity, sales_price)
            sales_goods_set.append(SalesGoods(
                sales_order=sales_order, goods=sales_goods_item['goods'], sales_quantity=sales_quantity,
                sales_price=sales_price, total_amount=total_amount, team=self.team
            ))

            total_sales_quantity = NP.plus(total_sales_quantity, sales_quantity)
            total_sales_amount = NP.plus(total_sales_amount, total_amount)
        else:
            SalesGoods.objects.bulk_create(sales_goods_set)
            total_sales_amount = NP.times(total_sales_amount, sales_order.discount, 0.01)
            total_sales_amount = NP.plus(total_sales_amount, sales_order.other_amount)
            sales_order.total_quantity = total_sales_quantity
            sales_order.total_amount = total_sales_amount

        total_collection_amount = 0

        if sales_account_items:
            # 販売決済口座を作成
            sales_accounts = []
            for sales_account_item in sales_account_items:
                collection_amount = sales_account_item['collection_amount']
                sales_accounts.append(SalesAccount(
                    sales_order=sales_order, account=sales_account_item['account'],
                    collection_amount=collection_amount, team=self.team
                ))

                total_collection_amount = NP.plus(total_collection_amount, collection_amount)
            else:
                SalesAccount.objects.bulk_create(sales_accounts)

        sales_order.collection_amount = total_collection_amount
        sales_order.arrears_amount = NP.minus(total_sales_amount, total_collection_amount)
        sales_order.save(update_fields=['total_quantity', 'total_amount', 'collection_amount',
                                        'arrears_amount'])
        return sales_order


class SalesReturnOrderSerializer(BaseSerializer):
    """販売返品伝票"""

    class SalesReturnGoodsItemSerializer(BaseSerializer):
        """販売返品商品"""

        goods_number = CharField(source='goods.number', read_only=True, label='商品コード')
        goods_name = CharField(source='goods.name', read_only=True, label='商品名')
        goods_barcode = CharField(source='goods.barcode', read_only=True, label='商品バーコード')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='単位名')

        class Meta:
            model = SalesReturnGoods
            read_only_fields = ['id', 'goods_number', 'goods_name', 'goods_barcode',
                                'total_amount', 'unit_name']
            fields = ['sales_goods', 'goods', 'return_quantity', 'return_price', *read_only_fields]

        def validate_sales_goods(self, instance):
            instance = self.validate_foreign_key(SalesGoods, instance, message='販売商品が存在しません')
            return instance

        def validate_goods(self, instance):
            instance = self.validate_foreign_key(Goods, instance, message='商品が存在しません')
            if not instance.is_active:
                raise ValidationError(f'商品[{instance.name}]は有効化されていません')
            return instance

        def validate_return_quantity(self, value):
            if value <= 0:
                raise ValidationError('返品数量がゼロ以下です')
            return value

        def validate_return_price(self, value):
            if value <= 0:
                raise ValidationError('返品単価がゼロ以下です')
            return value

    class SalesReturnAccountItemSerializer(BaseSerializer):
        """販売返品決済口座"""

        account_number = CharField(source='account.number', read_only=True, label='口座コード')
        account_name = CharField(source='account.name', read_only=True, label='口座名')

        class Meta:
            model = SalesReturnAccount
            read_only_fields = ['id', 'account_number', 'account_name']
            fields = ['account', 'payment_amount', *read_only_fields]

        def validate_account(self, instance):
            instance = self.validate_foreign_key(Account, instance, message='口座が存在しません')
            if not instance.is_active:
                raise ValidationError(f'口座[{instance.name}]は有効化されていません')
            return instance

        def validate_payment_amount(self, value):
            if value <= 0:
                raise ValidationError('支払金額がゼロ以下です')
            return value

    sales_order_number = CharField(source='sales_order.number', read_only=True, label='販売伝票番号')
    warehouse_number = CharField(source='warehouse.number', read_only=True, label='倉庫コード')
    warehouse_name = CharField(source='warehouse.name', read_only=True, label='倉庫名')
    client_number = CharField(source='client.number', read_only=True, label='顧客コード')
    client_name = CharField(source='client.name', read_only=True, label='顧客名')
    handler_name = CharField(source='handler.name', read_only=True, label='担当者名')
    creator_name = CharField(source='creator.name', read_only=True, label='作成者名')
    sales_return_goods_items = SalesReturnGoodsItemSerializer(
        source='sales_return_goods_set', many=True, label='販売返品商品')
    sales_return_account_items = SalesReturnAccountItemSerializer(
        source='sales_return_accounts', required=False, many=True, label='販売返品決済口座')

    class Meta:
        model = SalesReturnOrder
        read_only_fields = ['id', 'sales_order_number', 'warehouse_number', 'warehouse_name',
                            'client_number', 'client_name', 'handler_name', 'total_quantity',
                            'total_amount', 'payment_amount', 'arrears_amount', 'is_void',
                            'enable_auto_stock_in', 'creator', 'creator_name', 'create_time']
        fields = ['number', 'sales_order', 'warehouse', 'client', 'handler', 'handle_time',
                  'remark', 'other_amount', 'sales_return_goods_items',
                  'sales_return_account_items', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'番号[{value}]は既に存在します')
        return value

    def validate_sales_order(self, instance):
        instance = self.validate_foreign_key(SalesOrder, instance, message='販売伝票が存在しません')
        if instance.is_void:
            raise ValidationError(f'販売伝票[{instance.number}]は無効化されています')
        return instance

    def validate_warehouse(self, instance):
        instance = self.validate_foreign_key(Warehouse, instance, message='倉庫が存在しません')
        if not instance.is_active:
            raise ValidationError(f'倉庫[{instance.name}]は有効化されていません')

        return instance

    def validate_client(self, instance):
        instance = self.validate_foreign_key(Client, instance, message='顧客が存在しません')
        if not instance.is_active:
            raise ValidationError(f'顧客[{instance.name}]は有効化されていません')
        return instance

    def validate_handler(self, instance):
        instance = self.validate_foreign_key(User, instance, message='担当者が存在しません')
        if not instance.is_active:
            raise ValidationError(f'担当者[{instance.name}]は有効化されていません')
        return instance

    def validate_other_amount(self, value):
        if value < 0:
            raise ValidationError('その他費用がゼロ未満です')
        return value

    def validate(self, attrs):
        if sales_order := attrs.get('sales_order'):
            if sales_order.warehouse != attrs['warehouse']:
                raise ValidationError(f'販売伝票[{sales_order.number}]の選択が間違っています')

            if sales_order.client != attrs['client']:
                raise ValidationError(f'販売伝票[{sales_order.number}]の選択が間違っています')

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        sales_return_goods_items = validated_data.pop('sales_return_goods_set')
        sales_return_account_items = validated_data.pop('sales_return_accounts', [])

        validated_data['enable_auto_stock_in'] = self.team.enable_auto_stock_in
        validated_data['creator'] = self.user
        sales_return_order = super().create(validated_data)

        total_return_quantity = 0
        total_return_amount = 0

        # 販売返品商品を作成
        sales_return_goods_set = []
        for sales_return_goods_item in sales_return_goods_items:
            goods = sales_return_goods_item['goods']
            return_quantity = sales_return_goods_item['return_quantity']

            sales_goods = None
            if sales_order := sales_return_order.sales_order:
                if not (sales_goods := sales_return_goods_item.get('sales_goods')):
                    raise ValidationError(f'販売伝票[{sales_order.number}]に商品[{goods.name}]が存在しません')

                sales_goods.return_quantity = NP.plus(sales_goods.return_quantity, return_quantity)
                if sales_goods.return_quantity > sales_goods.sales_quantity:
                    raise ValidationError(f'返品商品[{goods.name}]の返品数量が間違っています')

                # 販売商品返品数量を同期
                sales_goods.save(update_fields=['return_quantity'])

            return_price = sales_return_goods_item['return_price']
            total_amount = NP.times(return_quantity, return_price)
            sales_return_goods_set.append(SalesReturnGoods(
                sales_return_order=sales_return_order, sales_goods=sales_goods,
                goods=goods, return_quantity=return_quantity, return_price=return_price,
                total_amount=total_amount, team=self.team
            ))

            total_return_quantity = NP.plus(total_return_quantity, return_quantity)
            total_return_amount = NP.plus(total_return_amount, total_amount)
        else:
            SalesReturnGoods.objects.bulk_create(sales_return_goods_set)
            total_return_amount = NP.plus(total_return_amount, sales_return_order.other_amount)
            sales_return_order.total_quantity = total_return_quantity
            sales_return_order.total_amount = total_return_amount

        total_payment_amount = 0

        if sales_return_account_items:
            # 販売返品決済口座を作成
            sales_return_accounts = []
            for sales_return_account_item in sales_return_account_items:
                payment_amount = sales_return_account_item['payment_amount']
                sales_return_accounts.append(SalesReturnAccount(
                    sales_return_order=sales_return_order, account=sales_return_account_item['account'],
                    payment_amount=payment_amount, team=self.team
                ))

                total_payment_amount = NP.plus(total_payment_amount, payment_amount)
            else:
                SalesReturnAccount.objects.bulk_create(sales_return_accounts)

        sales_return_order.payment_amount = total_payment_amount
        sales_return_order.arrears_amount = NP.minus(total_return_amount, total_payment_amount)
        sales_return_order.save(update_fields=['total_quantity', 'total_amount', 'payment_amount',
                                               'arrears_amount'])

        return sales_return_order


__all__ = [
    'SalesOrderSerializer', 'SalesReturnOrderSerializer',
]
