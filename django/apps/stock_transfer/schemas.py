from extensions.serializers import *


class NumberResponse(Serializer):
    number = CharField(label='番号')


__all__ = [
    'NumberResponse',
]
