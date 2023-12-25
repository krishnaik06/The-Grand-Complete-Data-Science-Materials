import pytest
from qtpy import PYQT5, PYQT6, PYSIDE2, PYSIDE6


@pytest.mark.skipif(PYQT5 or PYSIDE2, reason="Only available in Qt6 bindings")
def test_qtwebenginequick():
    """Test the qtpy.QtWebEngineQuick namespace"""

    QtWebEngineQuick = pytest.importorskip("qtpy.QtWebEngineQuick")

    assert QtWebEngineQuick.QtWebEngineQuick is not None
    assert QtWebEngineQuick.QQuickWebEngineProfile is not None
