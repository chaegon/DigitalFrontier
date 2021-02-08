import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
#from PyQt5.QtCore import QRect
from PyQt5 import uic

import pandas as pd
import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc

from server import kospi

class Fantastic4(QWidget):
    def __init__(self):
        super().__init__()
        self.initBaseUI()

    #def createChartBox(self):
    #    chart = QVBoxLayout(parent=myWindow)

    def initBaseUI(self):
        global lblTitle
        lblTitle = QLabel('현재 탭 이름', self)
        fontTitle = lblTitle.font()
        fontTitle.setPointSize(32)
        lblTitle.setFont(fontTitle)

        tab1 = QScrollArea() #QWidget()
        tab2 = QScrollArea()
        tab3 = QScrollArea()

        global tabMain
        tabMain = QTabWidget()
        tabMain.setTabPosition(QTabWidget.East)

        tabMain.addTab(tab1, '시장현황')
        tabMain.addTab(tab2, '관심종목')
        tabMain.addTab(tab3, '추천종목')
        tabMain.currentChanged.connect(self.tabMain_on_changed)

        vboxMain = QVBoxLayout()
        vboxMain.addWidget(lblTitle)
        vboxMain.addWidget(tabMain)
        self.setLayout(vboxMain)

        lblTitle.setText('시장현황')
        #self.initMarketInfo(tab1)
        modKospi = kospi.KOSPI()
        modKospi.drawChartMarketInfo(tab1)
        self.initStocks(tab2)
        self.initSuggests(tab3)

        self.setWindowTitle("판타스틱4")
        self.setGeometry(100, 100, 1400, 980)
        self.show()

    # tab1
    def initMarketInfo(self, wgtParent):
        print('시장현황')

        # 지수정보
        lblIndexes = QLabel('지수정보', wgtParent)
        fntIndexes = lblIndexes.font()
        fntIndexes.setPointSize(24)
        lblIndexes.setFont(fntIndexes)
        # lblIndexes.setFrameStyle(QFrame.Panel)
        # lblIndexes.move(10,10)

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        start = datetime.datetime(2020, 10, 1)
        end = datetime.datetime.now()
        kospi_df = web.DataReader("^KS11", "yahoo", start, end)
        index = kospi_df.index.astype('str')  # 캔들스틱 x축이 str로 들어감

        # X축 티커 숫자 20개로 제한
        ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

        # 그래프 title과 축 이름 지정
        ax.set_title('KOSPI INDEX', fontsize=22)
        ax.set_xlabel('Date')

        # 캔들차트 그리기
        candlestick2_ohlc(ax, kospi_df['Open'], kospi_df['High'],
                          kospi_df['Low'], kospi_df['Close'],
                          width=0.5, colorup='r', colordown='b')
        ax.legend()
        canvas = FigureCanvas(fig)
        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(lblIndexes)
        vbxIndexes.addWidget(canvas)
        canvas.draw()

        # 환율정보
        # lblExchanges = QLabel('환율정보', wgtParent)

        # vboxMarketInfo = QVBoxLayout()
        # vboxMarketInfo.addWidget(lblIndexs)
        # vboxMarketInfo.addWidget(lblExchanges)
        #
        # self.setLayout(vboxMarketInfo)

    # tab2
    def initStocks(self, wgtParent):
        print('관심종목')

        btnSearch = QPushButton('종목검색', wgtParent)
        btnSearch.move(800, 10)

    # tab3
    def initSuggests(self, wgtParent):
        print('추천종목')

        lblAIintro = QLabel('AI가 추천하는 투자 종목', wgtParent)
        fntAIintro = lblAIintro.font()
        fntAIintro.setPointSize(16)
        lblAIintro.setFont(fntAIintro)
        #lblAIintro.move(10,10)

        #QRect cropper(0, 0, 1000, 400)

        lblImg1 = QLabel('', wgtParent)
        lblImg1.setPixmap(self.getCroppedPixmap(r'./images/structure_dataset.png'))

        lblImg2 = QLabel('', wgtParent)
        lblImg2.setPixmap(self.getCroppedPixmap(r'./images/structure_normal.png'))

        lblImg3 = QLabel('', wgtParent)
        lblImg3.setPixmap(self.getCroppedPixmap(r'./images/structure_origin.png'))

        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(lblAIintro)
        vbxIndexes.addWidget(lblImg1)
        vbxIndexes.addWidget(lblImg2)
        vbxIndexes.addWidget(lblImg3)

    def getCroppedPixmap(self, sImagePath):
        imgTarget = QImage(sImagePath)
        imgCropped = imgTarget.copy(100, 20, 1300, 520)
        return QPixmap(imgCropped)


    def changeTab(self, nTabIdx):
        self.tabMain.setCurrentIndex(nTabIdx)

    def tabMain_on_changed(self, nTabIdx):
        sTabName = '(탭 이름)'

        if nTabIdx == 0:
            #self.initMarketInfo(tabMain.widget(nTabIdx))
            sTabName = '시장현황'
        elif nTabIdx == 1:
            #self.initStocks(tabMain.widget(nTabIdx))
            sTabName = '관심종목'
        elif nTabIdx == 2:
            #self.initSuggests(tabMain.widget(nTabIdx))
            sTabName = '추천종목'

        lblTitle.setText(sTabName)
        print('tabMain_on_changed ['+str(nTabIdx)+'] ' + sTabName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    sys.exit(app.exec_())