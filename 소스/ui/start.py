import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class Fantastic4(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setWindowTitle("판타스틱4")
        self.setGeometry(100,100,800,600)



if __name__ == '__main__' :
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    myWindow.show()
    app.exec_()