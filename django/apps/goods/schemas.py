from extensions.serializers import *


class NumberResponse(Serializer):
    number = CharField(label='コード')


class DownloadResponse(Serializer):
    file = FileField(label='Excelファイル')


class UploadRequest(Serializer):
    file = FileField(label='Excelファイル')


__all__ = [
    'NumberResponse', 'DownloadResponse', 'UploadRequest',
]
