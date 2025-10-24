from django.db import transaction
from django.conf import settings
from number_precision import NP
from functools import reduce
import re
from datetime import datetime, timedelta
from django.utils import timezone

# Pendulum の代替（Python 3.13 対応）
class PendulumCompat:
    """pendulum の最小限の互換レイヤー"""

    @staticmethod
    def today():
        now = timezone.now()
        return PendulumDateTime(now.replace(hour=0, minute=0, second=0, microsecond=0))

    @staticmethod
    def tomorrow():
        now = timezone.now()
        tomorrow = now + timedelta(days=1)
        return PendulumDateTime(tomorrow.replace(hour=0, minute=0, second=0, microsecond=0))

    @staticmethod
    def now():
        return PendulumDateTime(timezone.now())

class PendulumDateTime:
    """pendulum.DateTime の最小限のエミュレーション"""

    def __init__(self, dt):
        if isinstance(dt, datetime):
            self._dt = dt
        else:
            # 既に datetime 型の場合
            self._dt = dt

    def to_datetime_string(self):
        return self._dt.strftime('%Y-%m-%d %H:%M:%S')

    def to_date_string(self):
        """日付文字列を返す（YYYY-MM-DD形式）"""
        return self._dt.strftime('%Y-%m-%d')

    def format(self, fmt):
        # pendulum の形式を Python の strftime に変換
        fmt = fmt.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d')
        fmt = fmt.replace('HH', '%H').replace('mm', '%M').replace('ss', '%S')
        return self._dt.strftime(fmt)

    # 比較演算子のサポート
    def __lt__(self, other):
        if isinstance(other, PendulumDateTime):
            return self._dt < other._dt
        elif isinstance(other, datetime):
            return self._dt < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, PendulumDateTime):
            return self._dt <= other._dt
        elif isinstance(other, datetime):
            return self._dt <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PendulumDateTime):
            return self._dt > other._dt
        elif isinstance(other, datetime):
            return self._dt > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PendulumDateTime):
            return self._dt >= other._dt
        elif isinstance(other, datetime):
            return self._dt >= other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, PendulumDateTime):
            return self._dt == other._dt
        elif isinstance(other, datetime):
            return self._dt == other
        return NotImplemented

pendulum = PendulumCompat()


__all__ = [
    'transaction', 'settings', 'NP', 'pendulum', 're', 'reduce',
]
