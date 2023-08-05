"""
WSQL
====
An asynchronous DB API v2.0 compatible interface to MySQL
---------------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import defaultdict
from decimal import Decimal
import datetime
import struct
import _wsql


NULL = _wsql.constants.NULL

_FLAG_BINARY = _wsql.constants.FLAG_BINARY
_FLAG_SET = _wsql.constants.FLAG_SET


def bool_to_sql(_, value):
    """Convert a Python bool to an SQL literal."""
    return int(value)


def set_to_sql(connection, value):
    """Convert a Python set to an SQL literal."""
    return connection.quote(','.join(value)).decode(connection.charset)


def str_to_sql(connection, value):
    """Convert a string object to a sql string literal by using connection encoding."""
    return connection.quote(value.encode(connection.charset))


def bytes_to_sql(connection, value):
    """Convert a bytes object to a sql string literal"""
    return connection.quote(value)


def int_to_sql(_, value):
    """Convert a bytes object to a sql int literal"""
    return value


def float_to_sql(_, value):
    """Convert float to sql literal"""
    return '%.15g' % value


def decimal_to_sql(_, value):
    """Convert Decimal to sql literal"""
    return value


def sql_to_decimal(value):
    """Convert SQL literal to Decimal"""
    return Decimal(value.decode('ascii'))


def none_to_sql(*_):
    """Convert None to NULL."""
    return NULL


def timedelta_to_sql(_, obj):
    """Convert timedelta to a SQL literal"""
    total_seconds = obj.seconds
    seconds = total_seconds % 60
    minutes = (total_seconds // 60) % 60
    hours = (total_seconds // 3600) % 24
    if obj.days < 0:
        hours = -hours

    if obj.microseconds:
        return ("'%02d:%02d:%02d.%06d'" % (hours, minutes, seconds, obj.microseconds)).encode('ascii')
    return ("'%02d:%02d:%02d'" % (hours, minutes, seconds)).encode('ascii')


def datetime_to_sql(_, obj):
    """Convert a datetime to a SQL literal"""
    return obj.strftime("'%Y-%m-%d %H:%M:%S'").encode('ascii')


def sql_to_date(obj):
    """Convert a SQL literal to date"""
    return datetime.date(*map(int, obj.split(b'-')))


def _split_time(t):
    """split time to seconds and microseconds"""
    parts = t.split(b'.')
    hour, minutes, seconds = map(int, parts[0].split(b':'))
    if len(parts) == 2:
        mcs = int(parts[1].ljust(6, b'0'))
    else:
        mcs = 0
    return hour, minutes, seconds, mcs


def sql_to_datetime(obj):
    """Convert a SQL literal to datetime"""
    date_, time_ = obj.split(b' ')
    parts = [int(i) for i in date_.split(b'-')]
    parts.extend(_split_time(time_))
    return datetime.datetime(*parts)


def sql_to_timedelta(obj):
    """Convert a SQL literal to timedelta"""
    hours, minutes, seconds, mcs = _split_time(obj)
    delta = datetime.timedelta(
        days=-(hours < 0),
        hours=abs(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        microseconds=mcs)
    return delta


def sql_to_bit(value):
    """Returns BIT columntype as integer"""
    if len(value) < 8:
        value = b'\x00' * (8 - len(value)) + value
    return struct.unpack('>Q', value)[0]


def any_to_sql(connection, obj):
    """Convert any object to sql literal."""
    return str_to_sql(connection, str(obj))


def none_if_null(func):
    """decorator, call function only if value is not None, otherwise return None"""
    def _none_if_null(value):
        return value if value is None else func(value)
    _none_if_null.__name__ = func.__name__ + "_or_None_if_NULL"
    return _none_if_null


int_or_None_if_NULL = none_if_null(int)
float_or_None_if_NULL = none_if_null(float)
decimal_or_None_if_NULL = none_if_null(sql_to_decimal)
datetime_or_None_if_NULL = none_if_null(sql_to_datetime)
date_or_None_if_NULL = none_if_null(sql_to_date)
timedelta_or_None_if_NULL = none_if_null(sql_to_timedelta)
bytes_or_None_if_NULL = none_if_null(lambda x: x)
bit_or_None_if_NULL = none_if_null(sql_to_bit)


simple_type_encoders = {
    bool: bool_to_sql,
    bytes: bytes_to_sql,
    datetime.datetime: datetime_to_sql,
    datetime.timedelta: timedelta_to_sql,
    float: float_to_sql,
    int: int_to_sql,
    Decimal: decimal_to_sql,
    set: set_to_sql,
    str: str_to_sql,
    type(None): none_to_sql
}

# This is for MySQL column types that can be converted directly
# into Python types without having to look at metadata (flags,
# character sets, etc.). This should always be used as the last
# resort.
simple_field_decoders = {
    _wsql.constants.FIELD_TYPE_TINY_BLOB: bytes_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_MEDIUM_BLOB: bytes_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_LONG_BLOB: bytes_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_TINY: int_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_SHORT: int_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_LONG: int_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_INT24: int_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_LONGLONG: int_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_FLOAT: float_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_DOUBLE: float_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_DECIMAL: decimal_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_NEWDECIMAL: decimal_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_YEAR: int_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_TIMESTAMP: datetime_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_DATETIME: datetime_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_DATE: date_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_NEWDATE: date_or_None_if_NULL,
    _wsql.constants.FIELD_TYPE_TIME: timedelta_or_None_if_NULL,

    _wsql.constants.FIELD_TYPE_BIT: bit_or_None_if_NULL,
}

# Decoder protocol
# Each decoder is passed a field object.
# The decoder returns a single value:
# * A callable that given an SQL value, returns a Python object.
# This can be as simple as int or str, etc. If the decoder
# returns None, this decoder will be ignored and the next decoder
# on the stack will be checked.


def default_decoder(*_):
    """by default, convert to bytes"""
    return bytes_or_None_if_NULL


def default_encoder(_, value):
    """Convert an Instance to a string representation.  If the __str__()
    method produces acceptable output, then you don't need to add the
    class to conversions; it will be handled by the default
    converter. If the exact class is not found in conv, it will use the
    first class it can find for which obj is an instance.
    """
    try:
        conv = next(key for key in simple_type_encoders if isinstance(value, key))
    except StopIteration:
        return any_to_sql

    return simple_type_encoders.setdefault(type(value), conv)


def simple_decoder(_, field):
    """convert according to predefined rules"""
    return simple_field_decoders.get(field.type, None)


def simple_encoder(_, value):
    """convert according to predefined rules"""
    return simple_type_encoders.get(type(value), None)


character_types = {
    _wsql.constants.FIELD_TYPE_BLOB,
    _wsql.constants.FIELD_TYPE_STRING,
    _wsql.constants.FIELD_TYPE_VAR_STRING,
    _wsql.constants.FIELD_TYPE_VARCHAR,
    _wsql.constants.FIELD_TYPE_SET
}


def character_decoder(connection, field):
    """convert value of mysql string type to python associated python type"""
    if field.type not in character_types:
        return None

    if field.flags & _FLAG_BINARY:
        return bytes_or_None_if_NULL

    charset = connection.charset

    def char_to_str(s):
        return s.decode(charset)

    if field.flags & _FLAG_SET:
        return none_if_null(lambda x: {char_to_str(s) for s in x.split(b',') if s})

    return none_if_null(char_to_str)


default_decoders = [
    character_decoder,
    simple_decoder,
    default_decoder,
]

default_encoders = [
    simple_encoder,
    default_encoder,
]


def get_codec(connection, field, codecs):
    """
    select codec
    :param connection: the connection object
    :param field: the value to convert
    :param codecs: the list of codecs
    :return: the function to convert specified field
    :raises: connection.NotSupportedError if there is no known converted to field
    """
    for c in codecs:
        func = c(connection, field)
        if func:
            return func
    raise connection.NotSupportedError(("could not encode as SQL", field))


def iter_row_decoder(decoders, _, row):
    """
    convert mysql row to iterable object
    :param decoders: the row decoder
    :param row: the raw row"
    :return the formatted row with delayed eval
    :rtype: generator
    """
    if row is None:
        return None
    return (d(col) for d, col in zip(decoders, row))


def tuple_row_decoder(decoders, names, row):
    """
    convert mysql row to tuple
    :param decoders: the row decoder
    :param names: the field names
    :param row: the raw row"
    :return the formatted row list
    :rtype: tuple
    """
    if row is None:
        return None
    return tuple(iter_row_decoder(decoders, names, row))


class ObjectDict(defaultdict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def dict_row_decoder(decoders, names, row):
    """
    decode row as dict
    :param decoders: the row decoder
    :param names: field names
    :param row: the formatted row
    :return: the dict
    :rtype: dict
    """
    if row is None:
        return None

    def recursive_factory():
        return ObjectDict(recursive_factory)

    result = recursive_factory()

    for name, value in zip(names, iter_row_decoder(decoders, names, row)):
        if name[0] == '_':
            continue

        *patch, name = name.split('.')
        o = result
        for p in patch:
            o = o[p]
        o[name] = value
    return result


object_row_decoder = dict_row_decoder
default_row_formatter = tuple_row_decoder
