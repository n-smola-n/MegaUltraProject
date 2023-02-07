import sys
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize


class MyWidget(QMainWindow):
    def __init__(self):
        self.flag = True
        self.ll = [34.6887, 3.0311]
        self.met = []
        self.map_params = {'ll': ",".join(map(str, self.ll)),
                           'l': "sat",
                           'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
                           'z': 6,
                           'pt': '~'.join(self.met)}
        super().__init__()
        uic.loadUi('UI1.ui', self)
        self.initUI()

    def photo(self):
        self.map_params['pt'] = '~'.join(self.met)
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=self.map_params)

        self.map_file = "picture.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap('picture.png')
        self.image.setPixmap(self.pixmap)
        self.image.show()

    def initUI(self):
        self.image.move(50, 10)
        self.image.resize(700, 500)
        self.photo()
        self.gibrid_2.clicked.connect(self.search)
        self.shema.clicked.connect(self.change_spn)
        self.sputnik.clicked.connect(self.change_spn)
        self.gibrid.clicked.connect(self.change_spn)
        self.shema_2.clicked.connect(self.del_met)

    def del_met(self):
        self.met = []
        self.photo()

    def search(self):
        toponym_to_find = self.lineEdit.text()
        print(toponym_to_find)

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        print(response)

        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self.met.append(','.join((toponym_longitude, toponym_lattitude)))

        self.map_params['ll'] = ','.join((toponym_longitude, toponym_lattitude))
        self.photo()

    def change_spn(self):
        if self.sender().text() == 'Схема':
            self.map_params['l'] = 'map'
        if self.sender().text() == 'Спутник':
            self.map_params['l'] = 'sat'
        if self.sender().text() == 'Гибрид':
            self.map_params['l'] = 'skl'
        self.photo()

    def keyPressEvent(self, event):
        s = self.map_params['z']
        s = (17 - s) ** 2 / 100
        if event.key() == Qt.Key_PageUp and self.map_params['z'] < 17:
            self.map_params['z'] += 1
            self.photo()
        if event.key() == Qt.Key_PageDown and self.map_params['z'] > 0:
            self.map_params['z'] -= 1
            self.photo()
        if event.key() == Qt.Key_W or event.key() == 1062:
            self.ll[1] = self.ll[1] + s
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_S or event.key() == 1067:
            self.ll[1] = self.ll[1] - s
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_A or event.key() == 1060:
            self.ll[0] = self.ll[0] - s
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_D or event.key() == 1042:
            self.ll[0] = self.ll[0] + s
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        elif event.key() == Qt.Key_Z:
            self.map_params['l'] = 'sat'
            self.photo()
        elif event.key() == Qt.Key_X:
            self.map_params['l'] = 'map'
            self.photo()
        elif event.key() == Qt.Key_C:
            self.map_params['l'] = 'skl'
            self.photo()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
