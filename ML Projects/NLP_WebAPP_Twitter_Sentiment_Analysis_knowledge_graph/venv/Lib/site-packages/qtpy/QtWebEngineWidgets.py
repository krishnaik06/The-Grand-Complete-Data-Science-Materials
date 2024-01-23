# -----------------------------------------------------------------------------
# Copyright © 2014-2015 Colin Duquesnoy
# Copyright © 2009- The Spyder development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Provides QtWebEngineWidgets classes and functions."""

from . import (
    PYQT5,
    PYQT6,
    PYSIDE2,
    PYSIDE6,
    QtModuleNotInstalledError,
)


# To test if we are using WebEngine or WebKit
# NOTE: This constant is imported by other projects (e.g. Spyder), so please
# don't remove it.
WEBENGINE = True


if PYQT5:
    try:
        from PyQt5.QtWebEngineWidgets import QWebEnginePage
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        from PyQt5.QtWebEngineWidgets import QWebEngineSettings
        from PyQt5.QtWebEngineWidgets import QWebEngineScript

        # Based on the work at https://github.com/spyder-ide/qtpy/pull/203
        from PyQt5.QtWebEngineWidgets import QWebEngineProfile
    except ModuleNotFoundError as error:
        raise QtModuleNotInstalledError(
            name='QtWebEngineWidgets', missing_package='PyQtWebEngine'
        ) from error
elif PYQT6:
    try:
        from PyQt6.QtWebEngineWidgets import *
        from PyQt6.QtWebEngineCore import QWebEnginePage
        from PyQt6.QtWebEngineCore import QWebEngineSettings
        from PyQt6.QtWebEngineCore import QWebEngineProfile
        from PyQt6.QtWebEngineCore import QWebEngineScript
    except ModuleNotFoundError as error:
        raise QtModuleNotInstalledError(
            name='QtWebEngineWidgets', missing_package='PyQt6-WebEngine'
        ) from error
elif PYSIDE2:
    from PySide2.QtWebEngineWidgets import QWebEnginePage
    from PySide2.QtWebEngineWidgets import QWebEngineView
    from PySide2.QtWebEngineWidgets import QWebEngineSettings
    from PySide2.QtWebEngineWidgets import QWebEngineScript

    # Based on the work at https://github.com/spyder-ide/qtpy/pull/203
    from PySide2.QtWebEngineWidgets import QWebEngineProfile
elif PYSIDE6:
    from PySide6.QtWebEngineWidgets import *
    from PySide6.QtWebEngineCore import QWebEnginePage
    from PySide6.QtWebEngineCore import QWebEngineSettings
    from PySide6.QtWebEngineCore import QWebEngineProfile
    from PySide6.QtWebEngineCore import QWebEngineScript
