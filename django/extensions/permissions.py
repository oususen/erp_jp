from rest_framework.permissions import BasePermission
from extensions.exceptions import ValidationError
from apps.system.models import User
from apps.manage.models import SuperUser
from extensions.common.base import pendulum


class IsSuperUser(BasePermission):
    message = 'ログイン認証が必要です'

    def has_permission(self, request, view):
        if not isinstance(request.user, SuperUser):
            return False

        return True


class IsAuthenticated(BasePermission):
    message = 'ログイン認証が必要です'

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        if (expiry_time := request.user.team.expiry_time) < pendulum.now():
            raise ValidationError(f'期限切れです。有効期限: {expiry_time}')

        if not (request.user.is_manager or request.user.is_active):
            raise ValidationError('アカウントが有効化されていないため、操作を実行できません')

        return True


class IsManagerPermission(BasePermission):
    message = '管理者アカウントではありません'

    def has_permission(self, request, view):
        return request.user.is_manager


class ModelPermission(BasePermission):
    message = '操作権限が追加されていません'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class FunctionPermission(BasePermission):
    """機能権限"""

    message = '操作権限が追加されていません'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        if self.code in request.user.permissions:
            return True

        return False


class DataPermission:
    """データ権限"""

    @classmethod
    def has_permission(cls, request):
        if request.user.is_manager:
            return True

        if cls.code in request.user.permissions:
            return True
        return False


__all__ = [
    'IsSuperUser', 'IsAuthenticated', 'IsManagerPermission',
    'ModelPermission', 'FunctionPermission', 'DataPermission',
]
