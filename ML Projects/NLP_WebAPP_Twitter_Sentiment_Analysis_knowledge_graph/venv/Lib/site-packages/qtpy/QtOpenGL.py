# -----------------------------------------------------------------------------
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Provides QtOpenGL classes and functions."""

from . import PYQT5, PYQT6, PYSIDE2, PYSIDE6

if PYQT5:
    from PyQt5.QtOpenGL import *
    from PyQt5.QtGui import (
        QOpenGLBuffer,
        QOpenGLFramebufferObject,
        QOpenGLFramebufferObjectFormat,
        QOpenGLShader,
        QOpenGLShaderProgram,
        QOpenGLContext,
        QOpenGLContextGroup,
        QOpenGLDebugLogger,
        QOpenGLDebugMessage,
        QOpenGLPixelTransferOptions,
        QOpenGLTexture,
        QOpenGLTextureBlitter,
        QOpenGLVersionProfile,
        QOpenGLVertexArrayObject,
        QOpenGLWindow,
    )

    # These are not present on some architectures such as armhf
    try:
        from PyQt5.QtGui import QOpenGLTimeMonitor, QOpenGLTimerQuery
    except ImportError:
        pass
elif PYQT6:
    from PyQt6.QtOpenGL import *
    from PyQt6.QtGui import QOpenGLContext, QOpenGLContextGroup
elif PYSIDE6:
    from PySide6.QtOpenGL import *
    from PySide6.QtGui import QOpenGLContext, QOpenGLContextGroup
elif PYSIDE2:
    from PySide2.QtOpenGL import *
    from PySide2.QtGui import (
        QOpenGLBuffer,
        QOpenGLFramebufferObject,
        QOpenGLFramebufferObjectFormat,
        QOpenGLShader,
        QOpenGLShaderProgram,
        QOpenGLContext,
        QOpenGLContextGroup,
        QOpenGLDebugLogger,
        QOpenGLDebugMessage,
        QOpenGLPixelTransferOptions,
        QOpenGLTexture,
        QOpenGLTextureBlitter,
        QOpenGLVersionProfile,
        QOpenGLVertexArrayObject,
        QOpenGLWindow,
    )

    # These are not present on some architectures such as armhf
    try:
        from PySide2.QtGui import QOpenGLTimeMonitor, QOpenGLTimerQuery
    except ImportError:
        pass
