from PyQt5.QtWidgets import *
from math import cos


class WorldMap(QLabel):
    def __init__(self, parent_dialog, parent=None):
        super().__init__(parent)
        self.parent_form = parent_dialog

    def mousePressEvent(self, event):
        x_coord = event.x()
        y_coord = event.y()
        print(x_coord, y_coord)
        delta = 360 / pow(2, self.parent_form.zoom + 8)
        if x_coord > self.pixmap().width() // 2:
            degree_x = self.parent_form.cords[0] + delta * (x_coord - self.pixmap().width() // 2)
        else:
            degree_x = self.parent_form.cords[0] - delta * (self.pixmap().width() // 2 - x_coord)
        delta = 180 * cos(degree_x) / pow(2, self.parent_form.zoom + 8)
        if y_coord > self.pixmap().height() // 2:
            degree_y = self.parent_form.cords[1] - delta * (y_coord - self.pixmap().height() // 2)
        else:
            degree_y = self.parent_form.cords[1] + delta * (self.pixmap().height() // 2 - y_coord)
        print(degree_x, degree_y)
        print(self.parent_form.cords[0], self.parent_form.cords[0])
        self.parent_form.find_object_from_click(degree_x, degree_y)
