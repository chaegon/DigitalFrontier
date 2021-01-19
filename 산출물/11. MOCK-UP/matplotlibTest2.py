import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ctypes

form = uic.loadUiType('matplotlibTest2.ui')[0]

class WindowClass(QMainWindow, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(self.canvas)

        cb = QComboBox()
        cb = self.comboBox

        #self.comboBox.addItems(['Graph1', 'Graph2'])
        #self.comboBox.activated[str].connect(self.onComboBoxChanged)
        #self.onComboBoxChanged(self.comboBox.currentText())

        cb.addItems(['Graph1', 'Graph2'])
        cb.activated[str].connect(self.onComboBoxChanged)
        self.onComboBoxChanged(cb.currentText())

    def msgBox(self, text, title='Information', style=0):
	    return ctypes.windll.user32.MessageBoxW(None, text, title, style)

    def onComboBoxChanged(self, text) :
        if text == 'Graph1':
            self.doGraph1()
        elif text == 'Graph2':
            self.doGraph2()
            self.msgBox('Graph2')

    def doGraph1(self):
        x = np.arange(0, 10, 0.5)
        y1 = np.sin(x)
        y2 = np.cos(x)
        
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(x, y1, label="sin(x)")
        ax.plot(x, y2, label="cos(x)", linestyle="--")
        
        ax.set_xlabel("x")
        ax.set_xlabel("y")
        
        ax.set_title("sin & cos")
        ax.legend()
        
        self.canvas.draw()
    def doGraph2(self):
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = X**2 + Y**2
        
        self.fig.clear()
        
        ax = self.fig.gca(projection='3d')
        ax.plot_wireframe(X, Y, Z, color='black')
        self.canvas.draw()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()