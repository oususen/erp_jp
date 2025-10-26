from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from extensions.common.base import *
from extensions.common.schema import *
from extensions.common.schema import *
from extensions.common.base import *
from extensions.permissions import *
from extensions.exceptions import *
from extensions.viewsets import *
from apps.system.serializers import *
from apps.system.schemas import *
from apps.system.models import *


class PermissionGroupViewSet(BaseViewSet, ListModelMixin):
    """権限グループ"""

    serializer_class = PermissionGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    ordering = ['id']
    queryset = PermissionGroup.objects.all()

    def get_queryset(self):
        return self.queryset.prefetch_related('permissions').all()


class SystemConfigViewSet(FunctionViewSet):
    """システム設定"""

    permission_classes = [IsAuthenticated, IsManagerPermission]

    @extend_schema(responses={200: SystemConfigSerializer})
    @action(detail=False, methods=['get'])
    def configs(self, request, *args, **kwargs):
        """設定情報"""

        serializer = SystemConfigSerializer(instance=self.team, context=self.context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=SystemConfigSerializer, responses={200: SystemConfigSerializer})
    @action(detail=False, methods=['post'])
    def set_configs(self, request, *args, **kwargs):
        """設定を保存"""

        serializer = SystemConfigSerializer(instance=self.team, data=request.data, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(ModelViewSet):
    """ロール"""

    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    search_fields = ['name']
    queryset = Role.objects.all()

    @transaction.atomic
    def perform_update(self, serializer):
        role = serializer.save()

        # ユーザー権限を同期
        users = role.users.prefetch_related('roles', 'roles__permissions').all()
        for user in users:
            permissions = {permission.code for role in user.roles.all()
                           for permission in role.permissions.all()}
            user.permissions = list(permissions)
        else:
            User.objects.bulk_update(users, ['permissions'])

    @transaction.atomic
    def perform_destroy(self, instance):
        users = instance.users.all()
        instance.delete()

        # ユーザー権限を同期
        for user in users.prefetch_related('roles', 'roles__permissions').all():
            permissions = {permission.code for role in user.roles.all()
                           for permission in role.permissions.all()}
            user.permissions = list(permissions)
        else:
            User.objects.bulk_update(users, ['permissions'])


class UserViewSet(ModelViewSet):
    """ユーザー"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    filterset_fields = ['sex', 'is_active']
    search_fields = ['username', 'name', 'phone', 'email']
    ordering_fields = ['id', 'username', 'name']
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        if instance.is_manager:
            raise ValidationError('管理者アカウントを削除できません')

        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError(f'ユーザー[{instance.username}]は参照されているため削除できません')

    @extend_schema(request=None, responses={200: None})
    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        """パスワードリセット"""

        instance = self.get_object()
        instance.password = make_password('123456')
        instance.save(update_fields=['password'])

        return Response(status=status.HTTP_200_OK)


class UserActionViewSet(FunctionViewSet):
    """ユーザー操作"""

    @extend_schema(request=GetTokenRequest, responses={200: GetTokenResponse})
    @action(detail=False, methods=['post'], permission_classes=[], authentication_classes=[])
    def get_token(self, request, *args, **kwargs):
        """トークン取得"""

        serializer = GetTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        if not (user := User.objects.filter(team__number=validated_data['number'],
                                            username=validated_data['username']).first()):
            raise ValidationError('ユーザーが存在しません')

        if not check_password(validated_data['password'], user.password):
            raise AuthenticationFailed('パスワードが間違っています')

        if not user.is_active and not user.is_manager:
            raise ValidationError('ユーザーが有効化されていません')

        token = RefreshToken()
        token['user_id'] = user.id
        data = {'refresh': str(token), 'access': str(token.access_token)}

        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(request=RefreshTokenRequest, responses={200: RefreshTokenResponse})
    @action(detail=False, methods=['post'], permission_classes=[], authentication_classes=[])
    def refresh_token(self, request, *args, **kwargs):
        """トークンリフレッシュ"""

        serializer = RefreshTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            token = RefreshToken(validated_data['refresh'])
        except TokenError:
            raise NotAuthenticated('トークンが無効です')

        data = {'access': str(token.access_token)}
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: UserInfoResponse})
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def info(self, request, *args, **kwargs):
        """ユーザー情報"""

        serializer = UserInfoResponse(instance=self.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=SetPasswordRequest, responses={204: None})
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        """パスワード設定"""

        serializer = SetPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not check_password(validated_data['old_password'], self.user.password):
            raise AuthenticationFailed('パスワードが間違っています')

        self.user.password = make_password(validated_data['new_password'])
        self.user.save(update_fields=['password'])

        return Response(status=status.HTTP_200_OK)


__all__ = [
    'PermissionGroupViewSet',
    'SystemConfigViewSet',
    'RoleViewSet', 'UserViewSet', 'UserActionViewSet',
]
