import pytest
from qtpy import PYQT5, PYSIDE2


def test_qtwebchannel():
    """Test the qtpy.QtWebChannel namespace"""
    from qtpy import QtWebChannel

    assert QtWebChannel.QWebChannel is not None
    assert QtWebChannel.QWebChannelAbstractTransport is not None
