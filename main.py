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
        self.map_params = {'ll': ",".join(map(str, self.ll)),
                           'l': "sat",
                           'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
                           'z': 6}
        super().__init__()
        uic.loadUi('UI1.ui', self)
        self.initUI()

    def photo(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=self.map_params)

        self.map_file = "picture.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap('picture.png')
        self.image.setPixmap(self.pixmap)
        self.image.show()

    def search(self):
        pass



    def initUI(self):
        self.image.move(50, 10)
        self.image.resize(700, 500)
        self.photo()
        self.shema.clicked.connect(self.change_spn)
        self.sputnik.clicked.connect(self.change_spn)
        self.gibrid.clicked.connect(self.change_spn)

    def change_spn(self):
        if self.sender().text() == 'Схема':
            self.map_params['l'] = 'map'
        if self.sender().text() == 'Спутник':
            self.map_params['l'] = 'sat'
        if self.sender().text() == 'Гибрид':
            self.map_params['l'] = 'skl'
        self.photo()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.map_params['z'] += 1
            self.photo()
        if event.key() == Qt.Key_PageDown:
            self.map_params['z'] -= 1
            self.photo()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
