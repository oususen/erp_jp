from extensions.models import *


class InventoryFlow(Model):
    """库存流水"""

    class Type(TextChoices):
        """流水类型"""

        PURCHASE = ('purchase', '購買')
        VOID_PURCHASE = ('void_purchase', '廃棄購買')
        PURCHASE_RETURN = ('purchase_return', '購買返品')
        VOID_PURCHASE_RETURN = ('void_purchase_return', '廃棄購買返品')
        SALES = ('sales', '販売')
        VOID_SALES = ('void_sales', '廃棄販売')
        SALES_RETURN = ('sales_return', '販売返品')
        VOID_SALES_RETURN = ('void_sales_return', '廃棄販売返品')
        STOCK_IN = ('stock_in', '入庫')
        VOID_STOCK_IN = ('void_stock_in', '廃棄入庫')
        STOCK_OUT = ('stock_out', '出庫')
        VOID_STOCK_OUT = ('void_stock_out', '廃棄出庫')
        STOCK_CHECK = ('stock_check', '棚卸')
        VOID_STOCK_CHECK = ('void_stock_check', '廃棄棚卸')
        STOCK_TRANSFER_OUT = ('stock_transfer_out', '在庫振替転出')
        VOID_STOCK_TRANSFER_OUT = ('void_stock_transfer_out', '廃棄在庫振替転出')
        STOCK_TRANSFER_IN = ('stock_transfer_in', '在庫振替転入')
        VOID_STOCK_TRANSFER_IN = ('void_stock_transfer_in', '廃棄在庫振替転入')

    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='inventory_flows', verbose_name='倉庫')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='inventory_flows', verbose_name='製品')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='フロータイプ')
    quantity_before = FloatField(verbose_name='変更前数量')
    quantity_change = FloatField(verbose_name='変更数量')
    quantity_after = FloatField(verbose_name='変更後数量')

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='inventory_flows', verbose_name='購買伝票')
    void_purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                     related_name='void_inventory_flows', verbose_name='廃棄購買伝票')
    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='inventory_flows', verbose_name='購買返品伝票')
    void_purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                            related_name='void_inventory_flows', verbose_name='廃棄購買返品伝票')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='inventory_flows', verbose_name='販売伝票')
    void_sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                                  related_name='void_inventory_flows', verbose_name='廃棄販売伝票')
    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                    related_name='inventory_flows', verbose_name='販売返品伝票')
    void_sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                         related_name='void_inventory_flows', verbose_name='廃棄販売返品伝票')
    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE, null=True,
                                related_name='inventory_flows', verbose_name='入庫通知伝票')
    void_stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE, null=True,
                                     related_name='void_inventory_flows', verbose_name='廃棄入庫通知伝票')
    stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE, null=True,
                                 related_name='inventory_flows', verbose_name='出庫通知伝票')
    void_stock_out_order = ForeignKey('stock_out.StockOutOrder', on_delete=CASCADE, null=True,
                                      related_name='void_inventory_flows', verbose_name='廃棄出庫通知伝票')
    stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE, null=True,
                                   related_name='inventory_flows', verbose_name='棚卸伝票')
    void_stock_check_order = ForeignKey('stock_check.StockCheckOrder', on_delete=CASCADE, null=True,
                                        related_name='void_inventory_flows', verbose_name='廃棄棚卸伝票')
    stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                      related_name='inventory_flows', verbose_name='在庫振替伝票')
    void_stock_transfer_order = ForeignKey('stock_transfer.StockTransferOrder', on_delete=CASCADE, null=True,
                                           related_name='void_inventory_flows', verbose_name='廃棄在庫振替伝票')

    creator = ForeignKey('system.User', on_delete=PROTECT, related_name='inventory_flows', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='inventory_flows')


class FinanceFlow(Model):
    """财务流水"""

    class Type(TextChoices):
        """流水类型"""

        PURCHASE = ('purchase', '購買')
        VOID_PURCHASE = ('void_purchase', '廃棄購買')
        PURCHASE_RETURN = ('purchase_return', '購買返品')
        VOID_PURCHASE_RETURN = ('void_purchase_return', '廃棄購買返品')
        SALES = ('sales', '販売')
        VOID_SALES = ('void_sales', '廃棄販売')
        SALES_RETURN = ('sales_return', '販売返品')
        VOID_SALES_RETURN = ('void_sales_return', '廃棄販売返品')

        PAYMENT = ('payment', '支払')
        VOID_PAYMENT = ('void_payment', '廃棄支払')
        COLLECTION = ('collection', '入金')
        VOID_COLLECTION = ('void_collection', '廃棄入金')
        CHARGE = ('charge', '收支')
        VOID_CHARGE = ('void_charge', '作废收支')
        ACCOUNT_TRANSFER_OUT = ('account_transfer_out', '转账转出')
        VOID_ACCOUNT_TRANSFER_OUT = ('void_account_transfer_out', '作废转账转出')
        ACCOUNT_TRANSFER_IN = ('account_transfer_in', '转账转入')
        VOID_ACCOUNT_TRANSFER_IN = ('void_account_transfer_in', '作废转账转入')

    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='finance_flows', verbose_name='決済アカウント')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='フロータイプ')
    amount_before = FloatField(verbose_name='変更前残高')
    amount_change = FloatField(verbose_name='変更残高')
    amount_after = FloatField(verbose_name='変更後残高')

    purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                related_name='finance_flows', verbose_name='購買伝票')
    void_purchase_order = ForeignKey('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                     related_name='void_finance_flows', verbose_name='廃棄購買伝票')
    purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='finance_flows', verbose_name='購買返品伝票')
    void_purchase_return_order = ForeignKey('purchase.PurchaseReturnOrder', on_delete=CASCADE, null=True,
                                            related_name='void_finance_flows', verbose_name='廃棄購買返品伝票')
    sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                             related_name='finance_flows', verbose_name='販売伝票')
    void_sales_order = ForeignKey('sales.SalesOrder', on_delete=CASCADE, null=True,
                                  related_name='void_finance_flows', verbose_name='廃棄販売伝票')
    sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                    related_name='finance_flows', verbose_name='販売返品伝票')
    void_sales_return_order = ForeignKey('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                         related_name='void_finance_flows', verbose_name='廃棄販売返品伝票')

    payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE, null=True,
                               related_name='finance_flows', verbose_name='支払伝票')
    void_payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE, null=True,
                                    related_name='void_finance_flows', verbose_name='廃棄支払伝票')
    collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE, null=True,
                                  related_name='finance_flows', verbose_name='入金伝票')
    void_collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE, null=True,
                                       related_name='void_finance_flows', verbose_name='廃棄入金伝票')
    charge_order = ForeignKey('finance.ChargeOrder', on_delete=CASCADE, null=True,
                              related_name='finance_flows', verbose_name='収支伝票')
    void_charge_order = ForeignKey('finance.ChargeOrder', on_delete=CASCADE, null=True,
                                   related_name='void_finance_flows', verbose_name='廃棄収支伝票')
    account_transfer_record = ForeignKey('finance.AccountTransferRecord', on_delete=CASCADE, null=True,
                                         related_name='finance_flows', verbose_name='振替記録')
    void_account_transfer_record = ForeignKey('finance.AccountTransferRecord', on_delete=CASCADE, null=True,
                                              related_name='void_finance_flows', verbose_name='廃棄振替記録')

    creator = ForeignKey('system.User', on_delete=PROTECT, null=True,
                         related_name='finance_flows', verbose_name='作成者')
    create_time = DateTimeField(auto_now_add=True, verbose_name='作成日時')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='finance_flows')


__all__ = [
    'InventoryFlow', 'FinanceFlow',
]
