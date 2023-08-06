# encoding: utf-8

import pytz
from django.db import models


class TimestampField(models.DateTimeField):
    def from_db_value(self, value, expression, connection, context):
        if value is None or getattr(value, 'tzinfo', None) is not None:
            return value
        value = pytz.utc.localize(value)
        return value


