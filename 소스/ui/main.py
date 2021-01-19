import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame
from PyQt5 import uic

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

form_class = uic.loadUiType("main.ui")[0]


class Q2Q (QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.window_setting()

        self.btn_menu_toggle.clicked.connect(self.btn_menu_toggle_on_click)

    def window_setting(self):
        self.setWindowTitle('Q2Q :: Quarter to Quadruple')
        # self.move(300, 300)
        self.resize(1280, 800)
        self.show()

    def btn_menu_toggle_on_click(self, state):
        print('Left Menu ' + {True: "Narrow", False: "Wide"}[state])
        if state:
            print(self.objectName())
            self.frame_left_menu.resize(50, 800)
        else:
            self.frame_left_menu.resize(300, 800)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Q2Q()
    win.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
