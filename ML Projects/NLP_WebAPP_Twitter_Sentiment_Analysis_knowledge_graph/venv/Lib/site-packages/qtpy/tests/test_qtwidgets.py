"""Test QtWidgets."""

import sys

import pytest

from qtpy import PYQT5, PYQT_VERSION, QtCore, QtGui, QtWidgets
from qtpy.tests.utils import using_conda, not_using_conda


@pytest.mark.skipif(
    sys.platform.startswith('linux') and not_using_conda(),
    reason="Fatal Python error: Aborted on Linux CI when not using conda")
def test_qtextedit_functions(qtbot, pdf_writer):
    """Test functions mapping for QtWidgets.QTextEdit."""
    assert QtWidgets.QTextEdit.setTabStopWidth
    assert QtWidgets.QTextEdit.tabStopWidth
    assert QtWidgets.QTextEdit.print_
    textedit_widget = QtWidgets.QTextEdit(None)
    textedit_widget.setTabStopWidth(90)
    assert textedit_widget.tabStopWidth() == 90
    print_device, output_path = pdf_writer
    textedit_widget.print_(print_device)
    assert output_path.exists()


def test_qlineedit_functions():
    """Test functions mapping for QtWidgets.QLineEdit"""
    assert QtWidgets.QLineEdit.getTextMargins


def test_what_moved_to_qtgui_in_qt6():
    """Test that we move back what has been moved to QtGui in Qt6"""
    assert QtWidgets.QAction is not None
    assert QtWidgets.QActionGroup is not None
    assert QtWidgets.QFileSystemModel is not None
    assert QtWidgets.QShortcut is not None
    assert QtWidgets.QUndoCommand is not None


@pytest.mark.skipif(
    sys.platform.startswith('linux') and not_using_conda(),
    reason="Fatal Python error: Aborted on Linux CI when not using conda")
def test_qplaintextedit_functions(qtbot, pdf_writer):
    """Test functions mapping for QtWidgets.QPlainTextEdit."""
    assert QtWidgets.QPlainTextEdit.setTabStopWidth
    assert QtWidgets.QPlainTextEdit.tabStopWidth
    assert QtWidgets.QPlainTextEdit.print_
    plaintextedit_widget = QtWidgets.QPlainTextEdit(None)
    plaintextedit_widget.setTabStopWidth(90)
    assert plaintextedit_widget.tabStopWidth() == 90
    print_device, output_path = pdf_writer
    plaintextedit_widget.print_(print_device)
    assert output_path.exists()


def test_qapplication_functions():
    """Test functions mapping for QtWidgets.QApplication."""
    assert QtWidgets.QApplication.exec_


@pytest.mark.skipif(
    sys.platform.startswith('linux') and not_using_conda(),
    reason="Fatal Python error: Aborted on Linux CI when not using conda")
@pytest.mark.skipif(
    sys.platform == 'darwin' and sys.version_info[:2] == (3, 7),
    reason="Stalls on macOS CI with Python 3.7")
def test_qdialog_functions(qtbot):
    """Test functions mapping for QtWidgets.QDialog."""
    assert QtWidgets.QDialog.exec_
    dialog = QtWidgets.QDialog(None)
    QtCore.QTimer.singleShot(100, dialog.accept)
    dialog.exec_()


@pytest.mark.skipif(
    sys.platform.startswith('linux') and not_using_conda(),
    reason="Fatal Python error: Aborted on Linux CI when not using conda")
@pytest.mark.skipif(
    sys.platform == 'darwin' and sys.version_info[:2] == (3, 7),
    reason="Stalls on macOS CI with Python 3.7")
def test_qdialog_subclass(qtbot):
    """Test functions mapping for QtWidgets.QDialog when using a subclass"""
    assert QtWidgets.QDialog.exec_
    class CustomDialog(QtWidgets.QDialog):
        def __init__(self):
            super().__init__(None)
            self.setWindowTitle("Testing")
    assert CustomDialog.exec_
    dialog = CustomDialog()
    QtCore.QTimer.singleShot(100, dialog.accept)
    dialog.exec_()


@pytest.mark.skipif(
    sys.platform.startswith('linux') and not_using_conda(),
    reason="Fatal Python error: Aborted on Linux CI when not using conda")
@pytest.mark.skipif(
    sys.platform == 'darwin' and sys.version_info[:2] == (3, 7),
    reason="Stalls on macOS CI with Python 3.7")
def test_qmenu_functions(qtbot):
    """Test functions mapping for QtWidgets.QDialog."""
    assert QtWidgets.QMenu.exec_
    menu = QtWidgets.QMenu(None)
    QtCore.QTimer.singleShot(100, menu.close)
    menu.exec_()


@pytest.mark.skipif(PYQT5 and PYQT_VERSION.startswith('5.9'),
                    reason="A specific setup with at least sip 4.9.9 is needed for PyQt5 5.9.*"
                           "to work with scoped enum access")
def test_enum_access():
    """Test scoped and unscoped enum access for qtpy.QtWidgets.*."""
    assert QtWidgets.QFileDialog.AcceptOpen == QtWidgets.QFileDialog.AcceptMode.AcceptOpen
    assert QtWidgets.QMessageBox.InvalidRole == QtWidgets.QMessageBox.ButtonRole.InvalidRole
    assert QtWidgets.QStyle.State_None == QtWidgets.QStyle.StateFlag.State_None
    assert QtWidgets.QSlider.TicksLeft == QtWidgets.QSlider.TickPosition.TicksAbove
    assert QtWidgets.QStyle.SC_SliderGroove == QtWidgets.QStyle.SubControl.SC_SliderGroove
