"""Python 3.7 to 3.8 compatibility and platform compatibility."""

import os
import platform
import sys
import typing

PY38 = (sys.version_info < (3, 9))


Literal: typing.Any


if PY38:  # pragma: no cover
    # pytype not supported
    import unittest.mock

    Literal = unittest.mock.MagicMock(name='Literal')
else:  # pragma: no cover
    from typing import Literal

    Literal = Literal  # CAVEAT: use None instead of Literal[None]


def get_startupinfo() -> None:
    """Return None for startupinfo argument of ``subprocess.Popen``."""
    return None


assert get_startupinfo() is None, 'get_startupinfo() defaults to a no-op'


if platform.system() == 'Windows':  # pragma: no cover
    import subprocess

    def get_startupinfo() -> subprocess.STARTUPINFO:  # pytype: disable=module-attr
        """Return subprocess.STARTUPINFO instance hiding the console window."""
        startupinfo = subprocess.STARTUPINFO()  # pytype: disable=module-attr
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # pytype: disable=module-attr
        startupinfo.wShowWindow = subprocess.SW_HIDE  # pytype: disable=module-attr
        return startupinfo


def make_subprocess_arg(arg: typing.Union[str, os.PathLike]) -> typing.Union[str, os.PathLike]:
    """Return subprocess argument as is (default no-op)."""
    return arg


if platform.system() == 'Windows' and sys.version_info < (3, 8):  # pragma: no cover
    def make_subprocess_arg(arg: typing.Union[str, os.PathLike]) -> str:  # noqa: F811
        """Workaround https://bugs.python.org/issue41649 (not backported)."""
        return os.fspath(arg)
