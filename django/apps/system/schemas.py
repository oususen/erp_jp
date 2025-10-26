from extensions.serializers import *


class GetTokenRequest(Serializer):
    number = CharField(label='Teamコード')
    username = CharField(label='ユーザー名')
    password = CharField(label='パスワード')


class GetTokenResponse(Serializer):
    refresh = CharField(label='リフレッシュトークン')
    access = CharField(label='アクセストークン')


class RefreshTokenRequest(Serializer):
    refresh = CharField(label='リフレッシュトークン')


class RefreshTokenResponse(Serializer):
    access = CharField(label='アクセストークン')


class UserInfoResponse(Serializer):
    id = IntegerField(label='ユーザーID')
    username = CharField(label='ユーザー名')
    name = CharField(label='名称')
    is_manager = BooleanField(label='管理者ステータス')
    permissions = JSONField(label='権限')


class SetPasswordRequest(Serializer):
    old_password = CharField(label='旧パスワード')
    new_password = CharField(label='新パスワード')


__all__ = [
    'GetTokenRequest', 'GetTokenResponse',
    'RefreshTokenRequest', 'RefreshTokenResponse',
    'UserInfoResponse', 'SetPasswordRequest',
]
