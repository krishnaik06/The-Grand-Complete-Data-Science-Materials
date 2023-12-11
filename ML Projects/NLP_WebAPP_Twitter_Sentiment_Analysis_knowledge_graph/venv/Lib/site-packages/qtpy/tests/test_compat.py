"""Test the compat module."""
import pytest
import sys

from qtpy import compat, QtWidgets
from qtpy.tests.utils import not_using_conda

@pytest.mark.skipif(
    ((sys.version_info.major == 3 and sys.version_info.minor == 7)
    and sys.platform.startswith('win') and not not_using_conda()) 
    or
    (sys.platform.startswith('linux') and not_using_conda()),
    reason="sip not included in Python3.7 on Windows, or in non-conda test suite on Linux"
)
def test_isalive(qtbot):
    """Test compat.isalive"""
    test_widget = QtWidgets.QWidget()
    assert compat.isalive(test_widget) == True
    with qtbot.waitSignal(test_widget.destroyed):
        test_widget.deleteLater()
    assert compat.isalive(test_widget) == False
