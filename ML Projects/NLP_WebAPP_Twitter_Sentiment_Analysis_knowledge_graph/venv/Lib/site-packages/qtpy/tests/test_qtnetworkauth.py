import pytest

from qtpy import PYQT5, PYQT6, PYSIDE2


@pytest.mark.skipif(
    PYQT5 or PYQT6 or PYSIDE2,
    reason="Not available by default in PyQt. Not available for PySide2",
)
def test_qtnetworkauth():
    """Test the qtpy.QtNetworkAuth namespace"""
    QtNetworkAuth = pytest.importorskip("qtpy.QtNetworkAuth")

    assert QtNetworkAuth.QAbstractOAuth is not None
    assert QtNetworkAuth.QAbstractOAuth2 is not None
    assert QtNetworkAuth.QAbstractOAuthReplyHandler is not None
    assert QtNetworkAuth.QOAuth1 is not None
    assert QtNetworkAuth.QOAuth1Signature is not None
    assert QtNetworkAuth.QOAuth2AuthorizationCodeFlow is not None
