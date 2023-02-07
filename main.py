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
        print(response.status_code)
        self.map_file = "picture.png"

        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap('picture.png')
        self.image.setPixmap(self.pixmap)
        self.image.show()

    def initUI(self):
        self.image.move(100, -20)
        self.image.resize(600, 600)

        self.photo()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.map_params['z'] < 17:
            self.map_params['z'] += 1
            self.photo()
        if event.key() == Qt.Key_PageDown and self.map_params['z'] > 0:
            self.map_params['z'] -= 1
            self.photo()
        if event.key() == Qt.Key_Up:
            #self.ll = [34.6887, 3.0311]
            self.ll[1] = self.ll[1] + 0.0005
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_Down:
            self.ll[1] = self.ll[1] - 0.0005
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_Left:
            self.ll[0] = self.ll[0] - 0.0005
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        if event.key() == Qt.Key_Right:
            self.ll[0] = self.ll[0] + 0.0005
            self.map_params['ll'] = ",".join(map(str, self.ll))
            self.photo()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
