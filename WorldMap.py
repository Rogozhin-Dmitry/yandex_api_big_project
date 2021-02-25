from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import math
import requests


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


class WorldMap(QLabel):
    def __init__(self, parent_dialog, parent=None):
        super().__init__(parent)
        self.parent = parent_dialog

    def mousePressEvent(self, event):
        x_coord, y_coord = event.x() - 600 / 2, event.y() - self.size().height() / 2
        degree_for_pixel_x, degree_for_pixel_y = x_coord / (600 / 2), y_coord / (self.size().height() / 2)
        degree_x = self.parent.spn[0] * 1.07 * degree_for_pixel_x + self.parent.cords[0]
        degree_y = -self.parent.spn[1] * 0.6 * degree_for_pixel_y + self.parent.cords[1]
        if event.button() == Qt.LeftButton:
            self.parent.current_point = [degree_x, degree_y]
            self.parent.set_image()
            self.parent.find_object_from_click(degree_x, degree_y)
        elif event.button() == Qt.RightButton:
            self.parent.organization.setText('')
            response = requests.get(f"{self.parent.geo_coder_api_server}?geocode={degree_x},{degree_y}&format=json&" +
                                    "apikey=40d1649f-0493-4b70-98ba-98533de7710b")
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            adress = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
            search_api_server = "https://search-maps.yandex.ru/v1/"
            api_key = "f1896e00-0553-48a5-b3a2-e1be71681323"
            search_params = {
                "apikey": api_key,
                "text": adress,
                "lang": "ru_RU",
                "ll": ",".join([str(degree_x), str(degree_y)]),
                "type": "biz"
            }
            response = requests.get(search_api_server, params=search_params)
            if not response:
                pass
            json_response = response.json()
            try:
                organization = json_response["features"][0]
                point = organization["geometry"]["coordinates"]
                if lonlat_distance((degree_x, degree_y), point) <= 50:
                    self.parent.organization.setText(organization["properties"]["CompanyMetaData"]["name"])
                else:
                    self.parent.organization.setText("В районе 50 метров ничего не было найдено")
            except Exception as e:
                self.parent.organization.setText("В районе 50 метров ничего не было найдено")
