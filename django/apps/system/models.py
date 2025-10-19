from datetime import timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import EmailField
from django.utils import timezone
from extensions.models import *

class Team(Model):

    number = CharField(max_length=32, verbose_name='编号')
    expiry_time = DateTimeField(verbose_name='到期时间')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user_quantity = IntegerField(default=10, verbose_name='用户数量')
    remark = CharField(max_length=256, blank=True, null=True, verbose_name='备注')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='启用自动入库')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='启用自动出库')


class ERPUserManager(UserManager):
    """Adds default team assignment for superusers."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        team = extra_fields.get('team') or extra_fields.get('team_id')
        if not team:
            raise ValueError('User.team is required')
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        team = extra_fields.get('team')
        team_id = extra_fields.pop('team_id', None)
        if team is None and team_id:
            team = Team.objects.filter(pk=team_id).first()

        if team is None:
            team = Team.objects.order_by('id').first()

        if team is None:
            team = Team.objects.create(
                number='ADMIN',
                expiry_time=timezone.now() + timedelta(days=3650),
                user_quantity=1,
                enable_auto_stock_in=False,
                enable_auto_stock_out=False,
            )

        extra_fields['team'] = team
        extra_fields.setdefault('is_manager', True)

        return super().create_superuser(username, email, password, **extra_fields)


class PermissionGroup(Model):
    """权限分组"""

    name = CharField(max_length=64, verbose_name='分组名称')


class Permission(Model):
    """权限"""

    group = ForeignKey('system.PermissionGroup', on_delete=CASCADE, related_name='permissions', verbose_name='权限分组')
    name = CharField(max_length=64, verbose_name='权限名称')
    code = CharField(max_length=64, verbose_name='权限代码')


class Role(Model):
    """角色"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    permissions = ManyToManyField('system.Permission', blank=True, related_name='roles', verbose_name='权限')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='roles')

    class Meta:
        unique_together = [('name', 'team')]


class User(AbstractUser):
    """用户"""

    class Sex(TextChoices):
        """性别"""

        MAN = ('man', '男')
        WOMAN = ('woman', '女')

    username_validator = UnicodeUsernameValidator()

    username = CharField(
        max_length=150,
        unique=True,
        help_text='必填。150 字以内。可包含字母、数字和 @/./+/-/_ 等字符。',
        validators=[username_validator],
        verbose_name='用户名',
    )
    REQUIRED_FIELDS = ['name']
    objects = ERPUserManager()

    name = CharField(max_length=64, verbose_name='名称')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    email = EmailField(max_length=254, null=True, blank=True, verbose_name='邮箱')
    sex = CharField(max_length=32, choices=Sex.choices, verbose_name='性别')
    roles = ManyToManyField('system.Role', blank=True, related_name='users', verbose_name='角色')
    permissions = JSONField(default=list, verbose_name='权限')
    is_manager = BooleanField(default=False, verbose_name='管理员状态')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='users')

    class Meta(AbstractUser.Meta):
        unique_together = [('name', 'team')]

    def save(self, *args, **kwargs):
        self.is_staff = self.is_superuser or self.is_manager
        super().save(*args, **kwargs)


__all__ = [
    'Team', 'PermissionGroup', 'Permission', 'Role', 'User',
]
