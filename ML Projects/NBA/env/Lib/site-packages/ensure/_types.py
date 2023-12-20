from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from six import add_metaclass

USING_PYTHON2 = True if sys.version_info < (3, 0) else False

if USING_PYTHON2:
    str = unicode  # noqa

class NumericStringType(type):
    _type = str
    _cast = float

    def __instancecheck__(self, other):
        try:
            if not isinstance(other, self._type):
                raise TypeError()
            self._cast(other)
            return True
        except (TypeError, ValueError):
            return False

class NumericByteStringType(NumericStringType):
    _type = bytes

class IntegerStringType(NumericStringType):
    _cast = int

class IntegerByteStringType(IntegerStringType):
    _type = bytes

@add_metaclass(NumericStringType)
class NumericString(str):
    pass

@add_metaclass(NumericByteStringType)
class NumericByteString(bytes):
    pass

@add_metaclass(IntegerStringType)
class IntegerString(str):
    pass

@add_metaclass(IntegerByteStringType)
class IntegerByteString(bytes):
    pass
