# -----------------------------------------------------------------------------
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Provides access to sip."""

from . import (
    PYQT5,
    PYQT6,
    PYSIDE2,
    PYSIDE6,
    QtBindingMissingModuleError,
)

if PYQT5:
    from PyQt5.sip import *
elif PYQT6:
    from PyQt6.sip import *
elif PYSIDE2:
    raise QtBindingMissingModuleError(name='sip')
elif PYSIDE6:
    raise QtBindingMissingModuleError(name='sip')
