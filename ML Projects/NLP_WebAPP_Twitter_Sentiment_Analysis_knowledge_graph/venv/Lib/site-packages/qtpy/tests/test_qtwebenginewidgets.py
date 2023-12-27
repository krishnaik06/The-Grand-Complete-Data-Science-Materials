import pytest
from qtpy import PYSIDE6, PYQT6


@pytest.mark.skipif(PYSIDE6 or PYQT6, reason="Only available in Qt<6,>=6.2 bindings")
def test_qtwebenginewidgets():
    """Test the qtpy.QtWebEngineWidget namespace"""

    QtWebEngineWidgets = pytest.importorskip("qtpy.QtWebEngineWidgets")

    assert QtWebEngineWidgets.QWebEnginePage is not None
    assert QtWebEngineWidgets.QWebEngineView is not None
    assert QtWebEngineWidgets.QWebEngineSettings is not None
    assert QtWebEngineWidgets.QWebEngineScript is not None
