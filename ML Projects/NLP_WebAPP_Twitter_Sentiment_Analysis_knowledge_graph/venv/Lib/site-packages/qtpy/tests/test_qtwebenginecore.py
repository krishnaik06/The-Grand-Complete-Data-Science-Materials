import pytest
from qtpy import PYQT5, PYQT6, PYSIDE2, PYSIDE6


def test_qtwebenginecore():
    """Test the qtpy.QtWebEngineCore namespace"""
    QtWebEngineCore = pytest.importorskip("qtpy.QtWebEngineCore")

    assert QtWebEngineCore.QWebEngineHttpRequest is not None
