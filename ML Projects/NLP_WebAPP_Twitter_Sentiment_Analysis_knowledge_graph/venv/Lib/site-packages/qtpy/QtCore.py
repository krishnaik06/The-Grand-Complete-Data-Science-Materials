# -----------------------------------------------------------------------------
# Copyright © 2014-2015 Colin Duquesnoy
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Provides QtCore classes and functions."""
from typing import TYPE_CHECKING

from . import PYQT6, PYQT5, PYSIDE2, PYSIDE6

if PYQT5:
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtBoundSignal as SignalInstance
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import QT_VERSION_STR as __version__

    # For issue #153 and updated for issue #305
    from PyQt5.QtCore import QDate, QDateTime, QTime
    QDate.toPython = lambda self, *args, **kwargs: self.toPyDate(*args, **kwargs)
    QDateTime.toPython = lambda self, *args, **kwargs: self.toPyDateTime(*args, **kwargs)
    QTime.toPython = lambda self, *args, **kwargs: self.toPyTime(*args, **kwargs)

    # Those are imported from `import *`
    del pyqtSignal, pyqtBoundSignal, pyqtSlot, pyqtProperty, QT_VERSION_STR

elif PYQT6:
    from PyQt6 import QtCore
    from PyQt6.QtCore import *
    from PyQt6.QtCore import pyqtSignal as Signal
    from PyQt6.QtCore import pyqtBoundSignal as SignalInstance
    from PyQt6.QtCore import pyqtSlot as Slot
    from PyQt6.QtCore import pyqtProperty as Property
    from PyQt6.QtCore import QT_VERSION_STR as __version__

    # For issue #153 and updated for issue #305
    from PyQt6.QtCore import QDate, QDateTime, QTime
    QDate.toPython = lambda self, *args, **kwargs: self.toPyDate(*args, **kwargs)
    QDateTime.toPython = lambda self, *args, **kwargs: self.toPyDateTime(*args, **kwargs)
    QTime.toPython = lambda self, *args, **kwargs: self.toPyTime(*args, **kwargs)

    # For issue #311
    # Seems like there is an error with sip. Without first
    # trying to import `PyQt6.QtGui.Qt`, some functions like
    # `PyQt6.QtCore.Qt.mightBeRichText` are missing.
    if not TYPE_CHECKING:
        try:
            from PyQt6.QtGui import Qt
        except ImportError:
            pass

    # Map missing methods
    QCoreApplication.exec_ = QCoreApplication.exec
    QEventLoop.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
    QThread.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)

    QLibraryInfo.location = QLibraryInfo.path
    QLibraryInfo.LibraryLocation = QLibraryInfo.LibraryPath

    # Those are imported from `import *`
    del pyqtSignal, pyqtBoundSignal, pyqtSlot, pyqtProperty, QT_VERSION_STR

    # Allow unscoped access for enums inside the QtCore module
    from .enums_compat import promote_enums
    promote_enums(QtCore)
    del QtCore

    # Alias deprecated ItemDataRole enum values removed in Qt6
    Qt.BackgroundColorRole = Qt.ItemDataRole.BackgroundColorRole = Qt.BackgroundRole
    Qt.TextColorRole = Qt.ItemDataRole.TextColorRole = Qt.ForegroundRole
    # Alias for MiddleButton removed in PyQt6 but available in PyQt5, PySide2 and PySide6
    Qt.MidButton = Qt.MiddleButton

elif PYSIDE2:
    from PySide2.QtCore import *

    import PySide2.QtCore
    __version__ = PySide2.QtCore.__version__

    # Missing QtGui utility functions on Qt
    if getattr(Qt, 'mightBeRichText', None) is None:
        try:
            from PySide2.QtGui import Qt as guiQt
            Qt.mightBeRichText = guiQt.mightBeRichText
            del guiQt
        except ImportError:
            # Fails with PySide2 5.12.0
            pass

elif PYSIDE6:
    from PySide6.QtCore import *
    import PySide6.QtCore
    __version__ = PySide6.QtCore.__version__

    # Missing QtGui utility functions on Qt
    if getattr(Qt, 'mightBeRichText', None) is None:
        from PySide6.QtGui import Qt as guiQt
        Qt.mightBeRichText = guiQt.mightBeRichText
        del guiQt

    # Alias deprecated ItemDataRole enum values removed in Qt6
    Qt.BackgroundColorRole = Qt.ItemDataRole.BackgroundColorRole = Qt.BackgroundRole
    Qt.TextColorRole = Qt.ItemDataRole.TextColorRole = Qt.ForegroundRole
    Qt.MidButton = Qt.MiddleButton

    # Map DeprecationWarning methods
    QCoreApplication.exec_ = QCoreApplication.exec
    QEventLoop.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
    QThread.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
    QTextStreamManipulator.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
    QLibraryInfo.location = QLibraryInfo.path
    QLibraryInfo.LibraryLocation = QLibraryInfo.LibraryPath
