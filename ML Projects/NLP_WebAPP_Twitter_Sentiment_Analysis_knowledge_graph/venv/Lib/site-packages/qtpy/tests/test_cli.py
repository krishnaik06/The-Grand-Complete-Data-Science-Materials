"""Test the QtPy CLI."""

import subprocess
import sys

import pytest

import qtpy


SUBCOMMANDS = [
    [],
    ['mypy-args'],
]


@pytest.mark.parametrize(
    argnames=['subcommand'],
    argvalues=[[subcommand] for subcommand in SUBCOMMANDS],
    ids=[' '.join(subcommand) for subcommand in SUBCOMMANDS],
)
def test_cli_help_does_not_fail(subcommand):
    subprocess.run(
        [sys.executable, '-m', 'qtpy', *subcommand, '--help'], check=True,
    )


def test_cli_version():
    output = subprocess.run(
        [sys.executable, '-m', 'qtpy', '--version'],
        capture_output=True,
        check=True,
        encoding='utf-8',
    )
    assert output.stdout.strip().split()[-1] == qtpy.__version__


def test_cli_mypy_args():
    output = subprocess.run(
        [sys.executable, '-m', 'qtpy', 'mypy-args'],
        capture_output=True,
        check=True,
        encoding='utf-8',
    )

    if qtpy.PYQT5:
        expected = ' '.join([
            '--always-true=PYQT5',
            '--always-false=PYSIDE2',
            '--always-false=PYQT6',
            '--always-false=PYSIDE6',
        ])
    elif qtpy.PYSIDE2:
        expected = ' '.join([
            '--always-false=PYQT5',
            '--always-true=PYSIDE2',
            '--always-false=PYQT6',
            '--always-false=PYSIDE6',
        ])
    elif qtpy.PYQT6:
        expected = ' '.join([
            '--always-false=PYQT5',
            '--always-false=PYSIDE2',
            '--always-true=PYQT6',
            '--always-false=PYSIDE6',
        ])
    elif qtpy.PYSIDE6:
        expected = ' '.join([
            '--always-false=PYQT5',
            '--always-false=PYSIDE2',
            '--always-false=PYQT6',
            '--always-true=PYSIDE6',
        ])
    else:
        assert False, 'No valid API to test'

    assert output.stdout.strip() == expected.strip()
