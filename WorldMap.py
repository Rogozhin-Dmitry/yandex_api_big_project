from PyQt5.QtWidgets import *


class WorldMap(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_form = args[0]

    def mousePressEvent(self, event):
        x_coord = event.x()
        y_coord = event.y()
        degree_for_pixel_x = self.parent_form.spn[0] / self.size().width()
        degree_for_pixel_y = self.parent_form.spn[1] / self.size().height()
        degree_x = degree_for_pixel_x * x_coord
        degree_y = degree_for_pixel_y * y_coord
        # self.parent_form.find_object_from_click(degree_x, degree_y)
