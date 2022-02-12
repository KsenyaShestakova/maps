from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *


class Data(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.pushButton.clicked.connect(self.do)

    def do(self):
        self.ll = f'{self.input_d.text()},{self.input_sh.text()}'
        self.sc = self.scale.currentText()
