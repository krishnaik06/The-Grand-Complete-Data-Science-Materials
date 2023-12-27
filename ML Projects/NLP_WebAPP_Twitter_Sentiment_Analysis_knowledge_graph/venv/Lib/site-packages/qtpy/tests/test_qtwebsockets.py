import pytest
from qtpy import PYQT5, PYSIDE2


def test_qtwebsockets():
    """Test the qtpy.QtWebSockets namespace"""
    from qtpy import QtWebSockets

    assert QtWebSockets.QMaskGenerator is not None
    assert QtWebSockets.QWebSocket is not None
    assert QtWebSockets.QWebSocketCorsAuthenticator is not None
    assert QtWebSockets.QWebSocketProtocol is not None
    assert QtWebSockets.QWebSocketServer is not None
