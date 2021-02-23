import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QCursor
# from PyQt5.QtCore import QRect
# from PyQt5 import uic

from server import stock_code
from server import kospi
from server import server_main

import pandas as pd


class Fantastic4(QWidget):
    def __init__(self):
        super().__init__()
        self.initBaseUI()

    # def createChartBox(self):
    #    chart = QVBoxLayout(parent=myWindow)

    def initBaseUI(self):

        lblTitle = QLabel('현재 탭 이름', self)
        lblTitle.setObjectName('currentTitle')
        fontTitle = lblTitle.font()
        fontTitle.setPointSize(32)
        lblTitle.setFont(fontTitle)

        tab1 = QScrollArea() #QWidget()
        tab2 = QScrollArea()
        tab3 = QScrollArea()

        tabMain = QTabWidget()
        tabMain.setObjectName('tabMain')
        tabMain.setTabPosition(QTabWidget.North)

        tabMain.addTab(tab1, '시장현황')
        tabMain.addTab(tab2, '관심종목')
        tabMain.addTab(tab3, '추천종목')
        tabMain.currentChanged.connect(self.tabMain_on_changed)

        vboxMain = QVBoxLayout()
        vboxMain.addWidget(lblTitle)
        vboxMain.addWidget(tabMain)
        self.setLayout(vboxMain)

        lblTitle.setText('시장현황')
        self.initMarketInfo(tab1)
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

        wgtIndexes1 = QWidget()
        wgtIndexes2 = QWidget()

        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(lblIndexes)
        vbxIndexes.addWidget(wgtIndexes1)
        vbxIndexes.addWidget(wgtIndexes2)

        modKospi = kospi.KOSPI()
        modKospi.drawChartMarketInfo(wgtIndexes1, 'KOSPI', server_main.get_main_info_index())
        modKospi.drawChartMarketInfo(wgtIndexes2, 'KOSDAQ', server_main.get_main_info_index())

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
        grid = QGridLayout()

        fldKeyword = QLineEdit(wgtParent)
        fldKeyword.setObjectName('keyword')
        grid.addWidget(fldKeyword,0,0)
        # fldKeyword.move(60, 20)
        # fldKeyword.textChanged[str].connect(self.fldKeyword_on_changed)

        btnSearch = QPushButton('종목검색', wgtParent)
        grid.addWidget(btnSearch,0,1)
        # btnSearch.move(240, 20)
        btnSearch.clicked.connect(self.btnSearch_on_clicked)

        gboxStockInfoList = QGroupBox('종목검색결과')
        gboxStockInfoList.setObjectName('gboxStockInfoList')
        grid.addWidget(gboxStockInfoList,1,0)

        wgtParent.setLayout(grid)

    # draw stock information line from dataframe on target widget (not chart)
    def drawStockInfo (self, dict_stock_info, wgtParent):
        print(dict_stock_info)

        hbox = QHBoxLayout()
        for key, value in dict_stock_info.items():
            lblNew = QLabel(value)
            hbox.addWidget(lblNew)
        wgtParent.setLayout(hbox)
        return hbox

    # stock info click event
    def stock_info_on_click (self, stock_code):
        print(stock_code)

    # def fldKeyword_on_changed(self, sKeyword):
    def btnSearch_on_clicked(self, checked):
        gbox = self.findChild(QGroupBox, 'gboxStockInfoList')

        # find vbox previous defined
        vbox = self.findChild(QVBoxLayout, 'vboxStockInfoList')
        if vbox is None:
            # init vbox
            vbox = QVBoxLayout()
            vbox.setObjectName('vboxStockInfoList')
        else:
            # delete child widgets
            for i in reversed(range(vbox.count())):
                # vbox.itemAt(i).widget().deleteLater()
                vbox.itemAt(i).widget().setParent(None)

        fldKeyword = self.findChild(QLineEdit, 'keyword')
        sKeyword = fldKeyword.text()
        df_code_list = stock_code.getDataCodeName(sKeyword)
        bool_do_layout = False
        for code in df_code_list['code']:
            print(code)
            dict_stock_info = server_main.get_stock_realtime_info(code)
            # df_stock_info = pd.DataFrame([dict_stock_info])
            # print(dict_stock_info)
            wgt_new_stock_info = QPushButton()
            # wgt_new_stock_info.stock_code = code
            wgt_new_stock_info.setFixedHeight(40)
            self.drawStockInfo(dict_stock_info, wgt_new_stock_info)

            ### TODO! *** button clicked signal should set 'code' parameter each button ***
            wgt_new_stock_info.clicked.connect(lambda: self.stock_info_on_click(code))
            wgt_new_stock_info.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            vbox.addWidget(wgt_new_stock_info)
            bool_do_layout = True

        if bool_do_layout is True:
            # vbox.addStretch(1)  # 여백
            gbox.setLayout(vbox)

        print('\n>> end draw stock info list\n')

    # tab3
    def initSuggests(self, wgtParent):
        print('추천종목')

        lblAIintro = QLabel('종목 검색 후 선택하세요', wgtParent)
        # lblAIintro = QLabel('AI가 추천하는 투자 종목', wgtParent)
        fntAIintro = lblAIintro.font()
        fntAIintro.setPointSize(16)
        lblAIintro.setFont(fntAIintro)
        # lblAIintro.move(10,10)

        # QRect cropper(0, 0, 1000, 400)

        # lblImg1 = QLabel('', wgtParent)
        # lblImg1.setPixmap(self.getCroppedPixmap(r'./images/structure_dataset.png'))
        #
        # lblImg2 = QLabel('', wgtParent)
        # lblImg2.setPixmap(self.getCroppedPixmap(r'./images/structure_normal.png'))
        #
        # lblImg3 = QLabel('', wgtParent)
        # lblImg3.setPixmap(self.getCroppedPixmap(r'./images/structure_origin.png'))
        #
        # vbxIndexes = QVBoxLayout(wgtParent)
        # vbxIndexes.addWidget(lblAIintro)
        # vbxIndexes.addWidget(lblImg1)
        # vbxIndexes.addWidget(lblImg2)
        # vbxIndexes.addWidget(lblImg3)

    def getCroppedPixmap(self, sImagePath):
        imgTarget = QImage(sImagePath)
        imgCropped = imgTarget.copy(100, 20, 1300, 520)
        return QPixmap(imgCropped)

    def changeTab(self, nTabIdx):
        self.tabMain.setCurrentIndex(nTabIdx)

    def tabMain_on_changed(self, nTabIdx):
        sTabName = '(탭 이름)'

        # self.findChild(QTabWidget, 'tabMain')
        if nTabIdx == 0:
            # self.initMarketInfo(tabMain.widget(nTabIdx))
            sTabName = '시장현황'
        elif nTabIdx == 1:
            # self.initStocks(tabMain.widget(nTabIdx))
            sTabName = '관심종목'
        elif nTabIdx == 2:
            # self.initSuggests(tabMain.widget(nTabIdx))
            sTabName = '추천종목'

        lblTitle = self.findChild(QLabel, 'currentTitle')
        lblTitle.setText(sTabName)
        print('tabMain_on_changed ['+str(nTabIdx)+'] ' + sTabName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    sys.exit(app.exec_())