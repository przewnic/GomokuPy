# Author: przewnic

from PyQt5 import QtGui, QtCore


class Board():
    def __init__(self):
        self.size = {"width": 420, "height": 420}
        self.field_size = 30
        self.point_size = self.field_size//2
        self.points = []

    def draw_board(self, scene):
        # Draw vertical lines
        for point in range(self.size["height"]//self.field_size+1):
            scene.addLine(
                point*self.field_size, 0,
                point*self.field_size, self.size["height"]
                )
        # Draw horizontal lines
        for point in range(self.size["width"]//self.field_size+1):
            scene.addLine(
                0, point*self.field_size,
                self.size["width"], point*self.field_size
                )
        # Draw central point
        self.draw_point(
            self.size["width"]/2 - 2,
            self.size["height"]/2 - 2,
            "black", scene, size=4)

    def draw_point(self, x, y, color, scene, size=None):
        if not size:
            size = self.point_size
        item = scene.addEllipse(
            x, y, size, size,
            brush=QtGui.QBrush(QtGui.QColor(color), QtCore.Qt.SolidPattern))
        return item

    def is_beyond_board(self, x, y):
        """ Check if x,y position beyond board. """
        offset = self.point_size
        if x > self.size["width"] + offset:
            return True
        if y > self.size["height"] + offset:
            return True
        if x < -offset:
            return True
        if y < -offset:
            return True
        return False
