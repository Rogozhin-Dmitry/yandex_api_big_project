import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map_ui.ui', self)
        self.Get_Image.clicked.connect(self.new_param)
        self.geo_coder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"

        self.standard_spn = (0.006, 0.0045)
        self.spn = (0.006, 0.0045)
        self.cords = [37.530887, 55.703118]
        self.style = 'map'
        self.zoom = 0
        self.current_point = None

        self.map_file = ''
        self.pix_map = ''
        self.set_image()

    def new_param(self):
        self.zoom = self.Zoom.value() - 3
        self.style = self.comboBox.currentText()
        try:
            if self.radioButton.isChecked():
                response = requests.get(self.geo_coder_api_server +
                                        f"?geocode={self.Object.text()}&format=json&"
                                        f"apikey=40d1649f-0493-4b70-98ba-98533de7710b")
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
                self.current_point = [float(toponym_longitude), float(toponym_lattitude)]
                self.cords[0] = round(float(toponym_longitude), 6)
                self.cords[1] = round(float(toponym_lattitude), 6)
                self.Longitude.setText(str(round(float(toponym_longitude), 6)))
                self.Latitude.setText(str(round(float(toponym_lattitude), 6)))
            else:
                self.current_point = None
                self.cords[0] = round(float(self.Longitude.text()), 6)
                self.cords[1] = round(float(self.Latitude.text()), 6)
        except Exception as e:
            print('ошибка при вводе параметров', e)
            QMessageBox.critical(self, "Ошибка ", "Некорректное значение",
                                 QMessageBox.Ok)
        self.set_image()

    def set_image(self):
        self.spn = [i * 2 ** self.zoom for i in self.standard_spn]
        if self.current_point:
            response = requests.get(self.map_api_server +
                                    f"?ll={self.cords[0]},{self.cords[1]}&spn={self.spn[0]},"
                                    f"{self.spn[1]}&l={self.style}&pt={self.current_point[0]},"
                                    f"{self.current_point[1]},pmrdm")
        else:
            response = requests.get(self.map_api_server +
                                    f"?ll={self.cords[0]},{self.cords[1]}&"
                                    f"spn={self.spn[0]},{self.spn[1]}&l={self.style}")

        if not response:
            # print(f"Ошибка выполнения запроса:\nHttp статус:{response.status_code}, ({response.reason})")
            return 'error'
        else:
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.pix_map = QPixmap(self.map_file)
            self.map.setPixmap(self.pix_map)
        self.Zoom.setValue(self.zoom + 3)
        self.Longitude.setText(str(round(self.cords[0], 6)))
        self.Latitude.setText(str(round(self.cords[1], 6)))

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom != 12:
            self.zoom += 1
            self.update()
        elif event.key() == Qt.Key_PageDown and self.zoom != -3:
            self.zoom -= 1
            self.update()
        elif event.key() == Qt.Key_D:
            self.cords[0] += self.spn[0] * 2
            if self.set_image():
                self.cords[0] = 85.0
                # self.cords[0] -= self.spn[0] * 2
            self.update()
        elif event.key() == Qt.Key_A:
            self.cords[0] -= self.spn[0] * 2
            if self.set_image():
                self.cords[0] = -85.0
                # self.cords[0] += self.spn[0] * 2
            self.update()
        elif event.key() == Qt.Key_W:
            self.cords[1] += self.spn[1] * 2
            if self.set_image():
                self.cords[1] = 85.0
                # self.cords[1] -= self.spn[1] * 2
            self.update()
        elif event.key() == Qt.Key_S:
            self.cords[1] -= self.spn[1] * 2
            if self.set_image():
                self.cords[1] = -85.0
                # self.cords[1] += self.spn[1] * 2
            self.update()
        self.set_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
