import pytest


def test_qtdatavisualization():
    """Test the qtpy.QtDataVisualization namespace"""
    # Using import skip here since with Python 3 you need to install another package
    # besides the base `PyQt5` or `PySide2`.
    # For example in the case of `PyQt5` you need `PyQtDataVisualization`

    # QtDataVisualization
    QtDataVisualization = pytest.importorskip("qtpy.QtDataVisualization")
    assert QtDataVisualization.QScatter3DSeries is not None
    assert QtDataVisualization.QSurfaceDataItem is not None
    assert QtDataVisualization.QSurface3DSeries is not None
    assert QtDataVisualization.QAbstract3DInputHandler is not None
    assert QtDataVisualization.QHeightMapSurfaceDataProxy is not None
    assert QtDataVisualization.QAbstractDataProxy is not None
    assert QtDataVisualization.Q3DCamera is not None
    assert QtDataVisualization.QAbstract3DGraph is not None
    assert QtDataVisualization.QCustom3DVolume is not None
    assert QtDataVisualization.Q3DInputHandler is not None
    assert QtDataVisualization.QBarDataProxy is not None
    assert QtDataVisualization.QSurfaceDataProxy is not None
    assert QtDataVisualization.QScatterDataItem is not None
    assert QtDataVisualization.Q3DLight is not None
    assert QtDataVisualization.QScatterDataProxy is not None
    assert QtDataVisualization.QValue3DAxis is not None
    assert QtDataVisualization.Q3DBars is not None
    assert QtDataVisualization.QBarDataItem is not None
    assert QtDataVisualization.QItemModelBarDataProxy is not None
    assert QtDataVisualization.Q3DTheme is not None
    assert QtDataVisualization.QCustom3DItem is not None
    assert QtDataVisualization.QItemModelScatterDataProxy is not None
    assert QtDataVisualization.QValue3DAxisFormatter is not None
    assert QtDataVisualization.QItemModelSurfaceDataProxy is not None
    assert QtDataVisualization.Q3DScatter is not None
    assert QtDataVisualization.QTouch3DInputHandler is not None
    assert QtDataVisualization.QBar3DSeries is not None
    assert QtDataVisualization.QAbstract3DAxis is not None
    assert QtDataVisualization.Q3DScene is not None
    assert QtDataVisualization.QCategory3DAxis is not None
    assert QtDataVisualization.QAbstract3DSeries is not None
    assert QtDataVisualization.Q3DObject is not None
    assert QtDataVisualization.QCustom3DLabel is not None
    assert QtDataVisualization.Q3DSurface is not None
    assert QtDataVisualization.QLogValue3DAxisFormatter is not None

    # QtDatavisualization
    QtDatavisualization = pytest.importorskip("qtpy.QtDatavisualization")

    assert QtDatavisualization.QScatter3DSeries is not None
    assert QtDatavisualization.QSurfaceDataItem is not None
    assert QtDatavisualization.QSurface3DSeries is not None
    assert QtDatavisualization.QAbstract3DInputHandler is not None
    assert QtDatavisualization.QHeightMapSurfaceDataProxy is not None
    assert QtDatavisualization.QAbstractDataProxy is not None
    assert QtDatavisualization.Q3DCamera is not None
    assert QtDatavisualization.QAbstract3DGraph is not None
    assert QtDatavisualization.QCustom3DVolume is not None
    assert QtDatavisualization.Q3DInputHandler is not None
    assert QtDatavisualization.QBarDataProxy is not None
    assert QtDatavisualization.QSurfaceDataProxy is not None
    assert QtDatavisualization.QScatterDataItem is not None
    assert QtDatavisualization.Q3DLight is not None
    assert QtDatavisualization.QScatterDataProxy is not None
    assert QtDatavisualization.QValue3DAxis is not None
    assert QtDatavisualization.Q3DBars is not None
    assert QtDatavisualization.QBarDataItem is not None
    assert QtDatavisualization.QItemModelBarDataProxy is not None
    assert QtDatavisualization.Q3DTheme is not None
    assert QtDatavisualization.QCustom3DItem is not None
    assert QtDatavisualization.QItemModelScatterDataProxy is not None
    assert QtDatavisualization.QValue3DAxisFormatter is not None
    assert QtDatavisualization.QItemModelSurfaceDataProxy is not None
    assert QtDatavisualization.Q3DScatter is not None
    assert QtDatavisualization.QTouch3DInputHandler is not None
    assert QtDatavisualization.QBar3DSeries is not None
    assert QtDatavisualization.QAbstract3DAxis is not None
    assert QtDatavisualization.Q3DScene is not None
    assert QtDatavisualization.QCategory3DAxis is not None
    assert QtDatavisualization.QAbstract3DSeries is not None
    assert QtDatavisualization.Q3DObject is not None
    assert QtDatavisualization.QCustom3DLabel is not None
    assert QtDatavisualization.Q3DSurface is not None
    assert QtDatavisualization.QLogValue3DAxisFormatter is not None
