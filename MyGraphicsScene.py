# Author: przewnic

from PyQt5 import QtWidgets
from PyQt5 import QtCore


class MyGraphicsScene(QtWidgets.QGraphicsScene):
    mouse_released_pos = QtCore.pyqtSignal(QtCore.QPointF)
    mouse_hover_pos = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent):
        super(MyGraphicsScene, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        pos = event.lastScenePos()
        self.mouse_released_pos.emit(pos)

    def mouseMoveEvent(self, event):
        pos = event.lastScenePos()
        self.mouse_hover_pos.emit(pos)
