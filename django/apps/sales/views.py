from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.sales.serializers import *
from apps.sales.permissions import *
from apps.sales.filters import *
from apps.sales.schemas import *
from apps.sales.models import *
from apps.goods.models import *
from apps.flow.models import *
from apps.stock_out.models import *
from apps.stock_in.models import *


class SalesOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """販売伝票"""

    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, SalesOrderPermission]
    filterset_class = SalesOrderFilter
    search_fields = ['number', 'client__number', 'client__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['warehouse', 'client', 'handler', 'creator']
    prefetch_related_fields = ['sales_goods_set', 'sales_goods_set__goods',
                               'sales_goods_set__goods__unit',
                               'sales_accounts', 'sales_accounts__account']
    queryset = SalesOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        sales_order = serializer.save()

        if sales_order.enable_auto_stock_out:
            # 在庫と明細を同期
            inventory_flows = []
            for sales_goods in sales_order.sales_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_order.warehouse,
                                                  goods=sales_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_goods.sales_quantity
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_order.warehouse, goods=sales_goods.goods,
                    type=InventoryFlow.Type.SALES, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    sales_order=sales_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'商品[{inventory.goods.name}]の在庫が不足しています')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 出庫通知伝票を作成
            stock_out_order_number = StockOutOrder.get_number(team=self.team)
            stock_out_order = StockOutOrder.objects.create(
                number=stock_out_order_number, warehouse=sales_order.warehouse,
                type=StockOutOrder.Type.SALES, sales_order=sales_order,
                total_quantity=sales_order.total_quantity,
                remain_quantity=sales_order.total_quantity,
                creator=self.user, team=self.team
            )

            # 出庫商品を作成
            stock_out_goods_set = []
            for sales_goods in sales_order.sales_goods_set.all():
                stock_out_goods_set.append(StockOutGoods(
                    stock_out_order=stock_out_order, goods=sales_goods.goods,
                    stock_out_quantity=sales_goods.sales_quantity,
                    remain_quantity=sales_goods.sales_quantity, team=self.team
                ))
            else:
                StockOutGoods.objects.bulk_create(stock_out_goods_set)

        # 未払金を同期
        client = sales_order.client
        client.arrears_amount = NP.plus(client.arrears_amount, sales_order.arrears_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 口座と明細を同期
        if sales_order.collection_amount > 0:
            finance_flows = []
            for sales_account in sales_order.sales_accounts.all():
                account = sales_account.account
                amount_before = account.balance_amount
                amount_change = sales_account.collection_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.SALES, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after, sales_order=sales_order,
                    creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'決済口座[{account.name}]の残高が不足しています')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """番号取得"""

        number = SalesOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: SalesOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """無効化"""

        sales_order = self.get_object()
        if sales_order.is_void:
            raise ValidationError(f'販売伝票[{sales_order.number}]は既に無効化されているため、再度無効化できません')

        # 販売伝票と販売商品を同期
        sales_order.is_void = True
        sales_order.save(update_fields=['is_void'])

        if sales_order.enable_auto_stock_out:
            # 在庫と明細を同期
            inventory_flows = []
            for sales_goods in sales_order.sales_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_order.warehouse,
                                                  goods=sales_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_goods.sales_quantity
                quantity_after = NP.plus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_order.warehouse, goods=sales_goods.goods,
                    type=InventoryFlow.Type.VOID_SALES, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_sales_order=sales_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'商品[{inventory.goods.name}]の在庫が不足しています')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 出庫通知伝票を無効化
            stock_out_order = sales_order.stock_out_order
            if stock_out_order.total_quantity != stock_out_order.remain_quantity:
                raise ValidationError(f'販売伝票[{sales_order.number}]は出庫記録が存在するため無効化できません')

            stock_out_order.is_void = True
            stock_out_order.save(update_fields=['is_void'])

        # 未払金を同期
        client = sales_order.client
        client.arrears_amount = NP.minus(client.arrears_amount, sales_order.arrears_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 口座と明細を同期
        if sales_order.collection_amount > 0:
            finance_flows = []
            for sales_account in sales_order.sales_accounts.all():
                account = sales_account.account
                amount_before = account.balance_amount
                amount_change = sales_account.collection_amount
                amount_after = NP.minus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.VOID_SALES, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after, void_sales_order=sales_order,
                    creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'決済口座[{account.name}]の残高が不足しています')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = SalesOrderSerializer(instance=sales_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SalesReturnOrderViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """販売返品伝票"""

    serializer_class = SalesReturnOrderSerializer
    permission_classes = [IsAuthenticated, SalesReturnOrderPermission]
    filterset_class = SalesReturnOrderFilter
    search_fields = ['number', 'sales_order__number', 'client__number', 'client__name', 'remark']
    ordering_fields = ['id', 'number', 'total_quantity', 'total_amount', 'create_time']
    select_related_fields = ['sales_order', 'warehouse', 'client', 'handler', 'creator']
    prefetch_related_fields = ['sales_return_goods_set', 'sales_return_goods_set__goods',
                               'sales_return_goods_set__goods__unit',
                               'sales_return_accounts', 'sales_return_accounts__account']
    queryset = SalesReturnOrder.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        sales_return_order = serializer.save()

        if sales_return_order.enable_auto_stock_in:
            # 在庫と明細を同期
            inventory_flows = []
            for sales_return_goods in sales_return_order.sales_return_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_return_order.warehouse,
                                                  goods=sales_return_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_return_goods.return_quantity
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_return_order.warehouse, goods=sales_return_goods.goods,
                    type=InventoryFlow.Type.SALES_RETURN, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    sales_return_order=sales_return_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'商品[{inventory.goods.name}]の在庫が不足しています')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 入庫通知伝票を作成
            stock_in_order_number = StockInOrder.get_number(team=self.team)
            stock_in_order = StockInOrder.objects.create(
                number=stock_in_order_number, warehouse=sales_return_order.warehouse,
                type=StockInOrder.Type.SALES_RETURN, sales_return_order=sales_return_order,
                total_quantity=sales_return_order.total_quantity,
                remain_quantity=sales_return_order.total_quantity,
                creator=self.user, team=self.team
            )

            # 入庫商品を作成
            stock_in_goods_set = []
            for sales_return_goods in sales_return_order.sales_return_goods_set.all():
                stock_in_goods_set.append(StockInGoods(
                    stock_in_order=stock_in_order, goods=sales_return_goods.goods,
                    stock_in_quantity=sales_return_goods.return_quantity,
                    remain_quantity=sales_return_goods.return_quantity, team=self.team
                ))
            else:
                StockInGoods.objects.bulk_create(stock_in_goods_set)

        # 未払金を同期
        client = sales_return_order.client
        client.arrears_amount = NP.minus(client.arrears_amount, sales_return_order.arrears_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 口座と明細を同期
        if sales_return_order.payment_amount > 0:
            finance_flows = []
            for sales_return_account in sales_return_order.sales_return_accounts.all():
                account = sales_return_account.account
                amount_before = account.balance_amount
                amount_change = sales_return_account.payment_amount
                amount_after = NP.minus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.SALES_RETURN, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    sales_return_order=sales_return_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'決済口座[{account.name}]の残高が不足しています')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

    @extend_schema(responses={200: NumberResponse})
    @action(detail=False, methods=['get'])
    def number(self, request, *args, **kwargs):
        """番号取得"""

        number = SalesReturnOrder.get_number(self.team)
        return Response(data={'number': number}, status=status.HTTP_200_OK)

    @transaction.atomic
    @extend_schema(request=None, responses={200: SalesReturnOrderSerializer})
    @action(detail=True, methods=['post'])
    def void(self, request, *args, **kwargs):
        """無効化"""

        sales_return_order = self.get_object()
        if sales_return_order.is_void:
            raise ValidationError(f'販売返品伝票[{sales_return_order.number}]は既に無効化されているため、再度無効化できません')

        # 販売返品伝票と購買返品商品を同期
        sales_return_order.is_void = True
        sales_return_order.save(update_fields=['is_void'])

        if sales_return_order.enable_auto_stock_in:
            # 在庫と明細を同期
            inventory_flows = []
            for sales_return_goods in sales_return_order.sales_return_goods_set.all():
                inventory = Inventory.objects.get(warehouse=sales_return_order.warehouse,
                                                  goods=sales_return_goods.goods, team=self.team)
                quantity_before = inventory.total_quantity
                quantity_change = sales_return_goods.return_quantity
                quantity_after = NP.plus(quantity_before, quantity_change)

                inventory_flows.append(InventoryFlow(
                    warehouse=sales_return_order.warehouse, goods=sales_return_goods.goods,
                    type=InventoryFlow.Type.VOID_SALES_RETURN, quantity_before=quantity_before,
                    quantity_change=quantity_change, quantity_after=quantity_after,
                    void_sales_return_order=sales_return_order, creator=self.user, team=self.team
                ))

                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'商品[{inventory.goods.name}]の在庫が不足しています')
                inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['total_quantity', 'has_stock'])

                # 購買商品返品数量を同期
                if sales_goods := sales_return_goods.sales_goods:
                    sales_goods.return_quantity = NP.minus(sales_goods.return_quantity,
                                                           sales_return_goods.return_quantity)
                    sales_goods.save(update_fields=['return_quantity'])
            else:
                InventoryFlow.objects.bulk_create(inventory_flows)
        else:
            # 入庫通知伝票を無効化
            stock_in_order = sales_return_order.stock_in_order
            if stock_in_order.total_quantity != stock_in_order.remain_quantity:
                raise ValidationError(f'販売返品伝票[{sales_return_order.number}]は出庫記録が存在するため無効化できません')

            stock_in_order.is_void = True
            stock_in_order.save(update_fields=['is_void'])

        # 未払金を同期
        client = sales_return_order.client
        client.arrears_amount = NP.plus(client.arrears_amount, sales_return_order.arrears_amount)
        client.has_arrears = client.arrears_amount > 0
        client.save(update_fields=['arrears_amount', 'has_arrears'])

        # 口座と明細を同期
        if sales_return_order.payment_amount > 0:
            finance_flows = []
            for sales_return_account in sales_return_order.sales_return_accounts.all():
                account = sales_return_account.account
                amount_before = account.balance_amount
                amount_change = sales_return_account.payment_amount
                amount_after = NP.plus(amount_before, amount_change)

                finance_flows.append(FinanceFlow(
                    account=account, type=FinanceFlow.Type.VOID_SALES_RETURN, amount_before=amount_before,
                    amount_change=amount_change, amount_after=amount_after,
                    void_sales_return_order=sales_return_order, creator=self.user, team=self.team
                ))

                account.balance_amount = amount_after
                if account.balance_amount < 0:
                    raise ValidationError(f'決済口座[{account.name}]の残高が不足しています')
                account.has_balance = account.balance_amount > 0
                account.save(update_fields=['balance_amount', 'has_balance'])
            else:
                FinanceFlow.objects.bulk_create(finance_flows)

        serializer = SalesReturnOrderSerializer(instance=sales_return_order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'SalesOrderViewSet', 'SalesReturnOrderViewSet',
]
