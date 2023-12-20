#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BoxError(Exception):
    """Non standard dictionary exceptions"""


class BoxKeyError(BoxError, KeyError, AttributeError):
    """Key does not exist"""


class BoxTypeError(BoxError, TypeError):
    """Cannot handle that instance's type"""


class BoxValueError(BoxError, ValueError):
    """Issue doing something with that value"""


class BoxWarning(UserWarning):
    """Here be dragons"""
