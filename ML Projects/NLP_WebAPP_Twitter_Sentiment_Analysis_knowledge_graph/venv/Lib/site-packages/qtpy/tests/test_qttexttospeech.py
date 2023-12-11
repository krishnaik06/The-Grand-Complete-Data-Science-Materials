import pytest
from packaging import version
from qtpy import PYQT5, PYSIDE2, PYQT_VERSION


@pytest.mark.skipif(
    not ((PYQT5 and version.parse(PYQT_VERSION) >= version.parse("5.15.1")) or PYSIDE2),
    reason="Only available in Qt5 bindings (PyQt5 >= 5.15.1 or PySide2)",
)
def test_qttexttospeech():
    """Test the qtpy.QtTextToSpeech namespace."""
    from qtpy import QtTextToSpeech

    assert QtTextToSpeech.QTextToSpeech is not None
    assert QtTextToSpeech.QVoice is not None

    if PYSIDE2:
        assert QtTextToSpeech.QTextToSpeechEngine is not None
