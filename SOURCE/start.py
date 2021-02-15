import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import QRect
# from PyQt5 import uic

import pandas as pd

from server import kospi


class Fantastic4(QWidget):
    def __init__(self):
        super().__init__()
        self.initBaseUI()

        global df_code_name
        df_code_name = pd.read_csv('./data/code-name.csv')

    # def createChartBox(self):
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
        modKospi.drawChartMarketInfo(wgtIndexes1)
        modKospi.drawChartMarketInfo(wgtIndexes2)

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

        global fldKeyword
        fldKeyword = QLineEdit(wgtParent)
        fldKeyword.move(60, 20)
        # fldKeyword.textChanged[str].connect(self.fldKeyword_on_changed)

        btnSearch = QPushButton('종목검색', wgtParent)
        btnSearch.move(240, 20)
        btnSearch.clicked.connect(self.btnSearch_on_clicked)

    # def fldKeyword_on_changed(self, sKeyword):
    def btnSearch_on_clicked(self, checked):
        sKeyword = fldKeyword.text()
        print('검색어:'+sKeyword)
        # print(df_code_name.columns)

        list_search = []
        for idx, row in df_code_name[['code', 'name']].iterrows():
            for content in row:
                if sKeyword.strip() in content:
                    # print(idx)
                    list_search.append(df_code_name.loc[idx])
                    break

        df_search = pd.DataFrame(list_search, columns=df_code_name.columns).reset_index()
        print(df_search)

    # tab3
    def initSuggests(self, wgtParent):
        print('추천종목')

        lblAIintro = QLabel('AI가 추천하는 투자 종목', wgtParent)
        fntAIintro = lblAIintro.font()
        fntAIintro.setPointSize(16)
        lblAIintro.setFont(fntAIintro)
        # lblAIintro.move(10,10)

        # QRect cropper(0, 0, 1000, 400)

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
            # self.initMarketInfo(tabMain.widget(nTabIdx))
            sTabName = '시장현황'
        elif nTabIdx == 1:
            # self.initStocks(tabMain.widget(nTabIdx))
            sTabName = '관심종목'
        elif nTabIdx == 2:
            # self.initSuggests(tabMain.widget(nTabIdx))
            sTabName = '추천종목'

        lblTitle.setText(sTabName)
        print('tabMain_on_changed ['+str(nTabIdx)+'] ' + sTabName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    sys.exit(app.exec_())