import sys
import requests
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from sys import argv, exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PIL import Image
from PIL.ImageQt import ImageQt
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        uic.loadUi('main.ui', self)
        self.app = app
        self.pushButton.clicked.connect(self.change_map)
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.current_coords = [0, 0]
        self.current_size = 0
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"

    def change_map(self):
        try:
            if self.comboBox.currentText() == 'схема':
                style = 'map'
            elif self.comboBox.currentText() == 'спутник':
                style = 'sat'
            else:
                style = 'sat,skl'
            self.current_coords = [self.lineEdit.text().split(', ')[1], self.lineEdit.text().split(', ')[0]]
            self.current_size = str(0.01 * 2 ** self.spinBox.value())
            print(self.current_size)
            map_params = {
                "ll": ",".join(self.current_coords),
                # "z": self.current_size,
                "spn": ",".join([self.current_size, self.current_size]),
                "l": style,
            }
            response = requests.get(self.map_api_server, params=map_params)
            with open("map.png", "wb") as file:
                file.write(response.content)
            self.im_now = Image.open("map.png")
            self.b = ImageQt(self.im_now)
            self.pixmap = QPixmap.fromImage(self.b)
            self.image.setPixmap(self.pixmap)
        except Exception as e:
            print(e)
            self.error_label.setText('Извините вы ввели координаты неправильно')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spinBox.setValue(self.spinBox.value() - 1)
            self.change_map()
            self.update()
        elif event.key() == Qt.Key_PageDown:
            self.spinBox.setValue(self.spinBox.value() + 1)
            self.change_map()
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()

    sys.exit(app.exec())
    os.remove("map.png")
