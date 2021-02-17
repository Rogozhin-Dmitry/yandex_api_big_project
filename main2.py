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
        self.delete_2.clicked.connect(self.param)
        self.index.stateChanged.connect(self.new_param)
        self.geo_coder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.cords = [37.530887, 55.703118]
        self.style = 'map'
        self.zoom = 3
        self.current_point = None
        self.map_file = ''
        self.pix_map = ''
        self.set_image()

    def param(self):
        self.current_point = None
        self.Object.setText('')
        self.address.setText('Full address:')
        self.set_image()

    def new_param(self):
        self.zoom = self.Zoom.value()
        self.style = self.comboBox.currentText()
        try:
            if self.radioButton.isChecked():
                response = requests.get(f"{self.geo_coder_api_server}?geocode={self.Object.text()}&format=json&" +
                                        "apikey=40d1649f-0493-4b70-98ba-98533de7710b")

                if not response:
                    print(f"Ошибка выполнения запроса:\nHttp статус:{response.status_code}, ({response.reason})")
                else:
                    obj = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    self.address.setText(f'Full address: {obj["metaDataProperty"]["GeocoderMetaData"]["text"]}')
                    if self.index.isChecked():
                        try:
                            self.address.setText(self.address.text() + ' ' +
                                                 obj["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code'])
                        except Exception as e:
                            self.index.setCheckState(False)
                            print('ошибка при вводе параметров', e)
                            QMessageBox.critical(self, "Ошибка ", "У этого адреса нет индекса",
                                                 QMessageBox.Ok)
                    longitude, latitude = obj["Point"]["pos"].split()
                    self.current_point = [float(longitude), float(latitude)]
                    self.cords[0] = round(float(longitude), 6)
                    self.cords[1] = round(float(latitude), 6)
                    self.Longitude.setText(str(round(float(longitude), 6)))
                    self.Latitude.setText(str(round(float(latitude), 6)))
            else:
                self.cords[0] = round(float(self.Longitude.text()), 6)
                self.cords[1] = round(float(self.Latitude.text()), 6)
                self.Object.setText('')
                self.address.setText('Full address:')
        except Exception as e:
            print('ошибка при вводе параметров', e)
            QMessageBox.critical(self, "Ошибка ", "Некорректное значение",
                                 QMessageBox.Ok)
        self.set_image()

    def set_image(self):
        url = f"{self.map_api_server}?ll={self.cords[0]},{self.cords[1]}&z={self.zoom}&l={self.style}"
        if self.current_point:
            url += f"&pt={self.current_point[0]},{self.current_point[1]},pmrdm"
        response = requests.get(url)
        if not response:
            print(f"Ошибка выполнения запроса:\nHttp статус:{response.status_code}, ({response.reason})")
            return 'error'
        else:
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.pix_map = QPixmap(self.map_file)
            self.map.setPixmap(self.pix_map)
        self.Zoom.setValue(self.zoom)
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
            delta = 360 / pow(2, self.zoom + 8) * self.map.pixmap().width()
            self.cords[0] += delta
            if self.set_image():
                self.cords[0] = 85.0
            self.update()
        elif event.key() == Qt.Key_A:
            delta = 360 / pow(2, self.zoom + 8) * self.map.pixmap().width()
            self.cords[0] -= delta
            if self.set_image():
                self.cords[0] = -85.0
            self.update()
        elif event.key() == Qt.Key_W:
            delta = 360 / pow(2, self.zoom + 8) * self.map.pixmap().height()
            self.cords[1] += delta
            if self.set_image():
                self.cords[1] = 85.0
            self.update()
        elif event.key() == Qt.Key_S:
            delta = 360 / pow(2, self.zoom + 8) * self.map.pixmap().height()
            self.cords[1] -= delta
            if self.set_image():
                self.cords[1] = -85.0
            self.update()
        self.set_image()

    def find_object_from_click(self, degree_x, degree_y):
        response = requests.get(f"{self.geo_coder_api_server}?geocode={degree_x},{degree_y}&format=json&" +
                                "apikey=40d1649f-0493-4b70-98ba-98533de7710b")
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        name = toponym['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
        self.Object.setText(name)
        self.current_point = [degree_x, degree_y]
        self.address.setText(f'Full address: {toponym["metaDataProperty"]["GeocoderMetaData"]["text"]}')
        if self.index.isChecked():
            try:
                self.address.setText(self.address.text() + ' ' +
                                     toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code'])
            except Exception as e:
                self.index.setCheckState(False)
                print('ошибка при вводе параметров', e)
                QMessageBox.critical(self, "Ошибка ", "У этого адреса нет индекса", QMessageBox.Ok)
        self.set_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
