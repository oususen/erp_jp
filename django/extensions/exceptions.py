from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import APIException
from django.db.utils import IntegrityError
from rest_framework import status


class AuthenticationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '認証失敗'
    default_code = 'authentication_failed'


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '認証されていません'
    default_code = 'not_authenticated'


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '無効なリクエスト'
    default_code = 'invalid'


class ParseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'フォーマットエラー'
    default_code = 'parse_error'


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '操作を実行する権限がありません'
    default_code = 'permission_denied'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'データが存在しません'
    default_code = 'not_found'


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'サーバーエラー'
    default_code = 'server_error'


__all__ = [
    'ProtectedError', 'IntegrityError',
    'AuthenticationFailed', 'NotAuthenticated', 'ValidationError', 'ParseError',
    'PermissionDenied', 'NotFound', 'ServerError',
]
