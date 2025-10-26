from django.contrib.auth.hashers import make_password
from extensions.common.base import *
from extensions.serializers import *
from extensions.exceptions import *
from apps.system.models import *
from apps.goods.models import *


class PermissionGroupSerializer(BaseSerializer):

    class PermissionItemSerializer(BaseSerializer):

        class Meta:
            model = Permission
            fields = ['id', 'name', 'code']

    permission_items = PermissionItemSerializer(source='permissions', many=True, label='権限')

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name', 'permission_items']


class SystemConfigSerializer(BaseSerializer):

    class Meta:
        model = Team
        fields = ['enable_auto_stock_in', 'enable_auto_stock_out']

    def validate_enable_batch_control(self, value):
        if value and (self.team.enable_auto_stock_in or self.team.enable_auto_stock_out):
            raise ValidationError('自動入庫と自動出庫の両方を無効にした場合にのみ、商品のロット制御を有効にできます')
        return value

    def validate(self, attrs):
        if attrs['enable_auto_stock_in'] or attrs['enable_auto_stock_out']:
            if goods := Goods.objects.filter(enable_batch_control=True, team=self.team).first():
                raise ValidationError(f'商品[{goods.name}]はロット制御が有効になっているため、自動入出庫を有効にできません')
        return super().validate(attrs)


class RoleSerializer(BaseSerializer):

    class Meta:
        model = Role
        read_only_fields = ['id']
        fields = ['name', 'remark', 'permissions', *read_only_fields]

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]は既に存在します')
        return value


class UserSerializer(BaseSerializer):

    class RoleItemSerializer(BaseSerializer):

        class Meta:
            model = Role
            fields = ['id', 'name']

    sex_display = CharField(source='get_sex_display', read_only=True, label='性別')
    role_items = RoleItemSerializer(source='roles', many=True, read_only=True, label='ロールItem')

    class Meta:
        model = User
        read_only_fields = ['id', 'sex_display', 'is_manager', 'role_items', 'permissions', 'create_time']
        fields = ['username', 'name', 'phone', 'email', 'sex', 'roles', 'is_active', *read_only_fields]

    def validate_username(self, value):
        self.validate_unique({'username': value}, message=f'ユーザー名[{value}]は既に存在します')
        return value

    def validate_name(self, value):
        self.validate_unique({'name': value}, message=f'名称[{value}]は既に存在します')
        return value

    def validate_roles(self, instances):
        instances = self.validate_foreign_key_set(Role, instances, message='ロールが存在しません')
        return instances

    def create(self, validated_data):
        if self.team.users.count() >= self.team.user_quantity:
            raise ValidationError('ユーザー数が上限に達したため、ユーザーを作成できません')

        validated_data['password'] = make_password('123456')
        return super().create(validated_data)

    def save(self, **kwargs):
        permissions = []
        if roles := self.validated_data.get('roles'):
            permissions = {permission.code for role in roles.prefetch_related('permissions').all()
                           for permission in role.permissions.all()}

        kwargs['permissions'] = list(permissions)
        return super().save(**kwargs)


__all__ = [
    'PermissionGroupSerializer',
    'SystemConfigSerializer',
    'RoleSerializer', 'UserSerializer',
]
