import sys

import pytest

from qtpy import PYSIDE6, PYQT6


@pytest.mark.skipif(
    sys.platform.startswith("linux") and (PYSIDE6 or PYQT6),
    reason="Needs to setup GStreamer on Linux",
)
def test_qtmultimedia():
    """Test the qtpy.QtMultimedia namespace"""
    from qtpy import QtMultimedia

    assert QtMultimedia.QAudio is not None
    assert QtMultimedia.QAudioInput is not None

    if not (PYSIDE6 or PYQT6):
        assert QtMultimedia.QAbstractVideoBuffer is not None
        assert QtMultimedia.QAudioDeviceInfo is not None
        assert QtMultimedia.QSound is not None
