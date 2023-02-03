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
        self.PARAM = [34.6887, 3.0311, 0.009, 'sat']
        super().__init__()
        uic.loadUi('UI1.ui', self)
        self.initUI()

    def photo(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.PARAM[0]}," \
                      f"{self.PARAM[1]}&spn={self.PARAM[2]},0.002&l={self.PARAM[3]}"
        response = requests.get(map_request)
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
        if event.key() == Qt.Key_PageUp:
            self.PARAM[2] += 0.005
            self.photo()
        if event.key() == Qt.Key_PageDown:
            self.PARAM[2] -= 0.005
            self.photo()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
