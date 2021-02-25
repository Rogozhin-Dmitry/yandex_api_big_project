from PyQt5.QtWidgets import *


class WorldMap(QLabel):
    def __init__(self, parent_dialog, parent=None):
        super().__init__(parent)
        self.parent = parent_dialog

    def mousePressEvent(self, event):
        x_coord, y_coord = event.x() - 600 / 2, event.y() - self.size().height() / 2
        degree_for_pixel_x, degree_for_pixel_y = x_coord / (600 / 2), y_coord / (self.size().height() / 2)
        degree_x = self.parent.spn[0] * 1.07 * degree_for_pixel_x + self.parent.cords[0]
        degree_y = -self.parent.spn[1] * 0.6 * degree_for_pixel_y + self.parent.cords[1]
        self.parent.current_point = [[degree_x, degree_y]]
        self.parent.set_image()
        self.parent.find_object_from_click()
