import pytest
from qtpy import PYQT5, PYSIDE2


def test_qtquickwidgets():
    """Test the qtpy.QtQuickWidgets namespace"""
    from qtpy import QtQuickWidgets

    assert QtQuickWidgets.QQuickWidget is not None
