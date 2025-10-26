from extensions.common.base import *
from extensions.models import *


class Warehouse(Model):
    """倉庫"""

    number = CharField(max_length=32, verbose_name='番号')
    name = CharField(max_length=64, verbose_name='名称')
    manager = ForeignKey('system.User', on_delete=CASCADE, null=True,
                         related_name='warehouses', verbose_name='管理者')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='電話')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='住所')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    is_active = BooleanField(default=True, verbose_name='有効状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='warehouses')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'W001'
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


class Client(Model):
    """顧客"""

    class Level(TextChoices):
        """等級"""

        LEVEL0 = ('0', '通常顧客')
        LEVEL1 = ('1', '一級顧客')
        LEVEL2 = ('2', '二級顧客')
        LEVEL3 = ('3', '三級顧客')

    number = CharField(max_length=32, verbose_name='番号')
    name = CharField(max_length=64, verbose_name='名称')
    level = CharField(max_length=32, choices=Level.choices, default=Level.LEVEL0, verbose_name='等級')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='連絡先')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='携帯番号')
    email = CharField(max_length=256, null=True, blank=True, verbose_name='メールアドレス')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='住所')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    is_active = BooleanField(default=True, verbose_name='有効状態')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期未払金額')
    arrears_amount = AmountField(default=0, verbose_name='未払金額')
    has_arrears = BooleanField(default=False, verbose_name='未払い状況')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='clients')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'C001'
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


class Supplier(Model):
    """仕入先"""

    number = CharField(max_length=32, verbose_name='番号')
    name = CharField(max_length=64, verbose_name='名称')
    contact = CharField(max_length=64, null=True, blank=True, verbose_name='連絡先')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='携帯番号')
    email = CharField(max_length=256, null=True, blank=True, verbose_name='メールアドレス')
    address = CharField(max_length=256, null=True, blank=True, verbose_name='住所')
    bank_account = CharField(max_length=64, null=True, blank=True, verbose_name='銀行口座')
    bank_name = CharField(max_length=64, null=True, blank=True, verbose_name='取引銀行')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    is_active = BooleanField(default=True, verbose_name='有効状態')
    initial_arrears_amount = AmountField(default=0, verbose_name='初期未払金額')
    arrears_amount = AmountField(default=0, verbose_name='未払金額')
    has_arrears = BooleanField(default=False, verbose_name='未払い状況')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='suppliers')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'S001'
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


class Account(Model):
    """決済口座"""

    class Type(TextChoices):
        """口座タイプ"""

        CASH = ('cash', '現金')
        ALIPAY = ('alipay', 'Alipay')
        WECHAT = ('wechat', 'WeChat')
        BANK_ACCOUNT = ('bank_account', '銀行口座')
        OTHER = ('other', 'その他')

    number = CharField(max_length=32, verbose_name='番号')
    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, default=Type.CASH, verbose_name='口座タイプ')
    holder = CharField(max_length=64, null=True, blank=True, verbose_name='口座名義人')
    card_number = CharField(max_length=64, null=True, blank=True, verbose_name='口座番号')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    is_active = BooleanField(default=True, verbose_name='有効状態')
    initial_balance_amount = AmountField(default=0, verbose_name='初期残高')
    balance_amount = AmountField(default=0, verbose_name='残高')
    has_balance = BooleanField(default=False, verbose_name='残高状態')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='accounts')

    class Meta:
        unique_together = [('number', 'team'), ('name', 'team')]

    @classmethod
    def get_number(cls, team):
        default_number = 'A001'
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


class ChargeItem(Model):
    """収支項目"""

    class Type(TextChoices):
        """収支タイプ"""

        INCOME = ('income', '収入')
        EXPENDITURE = ('expenditure', '支出')

    name = CharField(max_length=64, verbose_name='名称')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='収支タイプ')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='備考')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='charge_items')

    class Meta:
        unique_together = [('name', 'team')]


__all__ = [
    'Warehouse', 'Client', 'Supplier', 'Account', 'ChargeItem',
]
