import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic


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
        fontTitle.setPointSize(20)
        lblTitle.setFont(fontTitle)

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        global tabMain
        tabMain = QTabWidget()
        tabMain.setTabPosition(QTabWidget.West)
        tabMain.addTab(tab1, '시장현황')
        tabMain.addTab(tab2, '관심종목')
        tabMain.addTab(tab3, '추천종목')
        tabMain.currentChanged.connect(self.tabMain_on_changed)

        vboxMain = QVBoxLayout()
        vboxMain.addWidget(lblTitle)
        vboxMain.addWidget(tabMain)
        self.setLayout(vboxMain)

        self.initMarketInfo(tab1)

        self.setWindowTitle("판타스틱4")
        self.setGeometry(100, 100, 1000, 800)
        self.show()

    # tab1
    def initMarketInfo(self, wgtParent):
        print('시장현황')
        lblTitle.setText('시장현황')

        # 지수정보
        lblIndexs = QLabel('지수정보', wgtParent)
        lblIndexs.setFrameStyle(QFrame.Panel)

        # 환율정보
        # lblExchanges = QLabel('환율정보', wgtParent)


        # vboxMarketInfo = QVBoxLayout()
        # vboxMarketInfo.addWidget(lblIndexs)
        # vboxMarketInfo.addWidget(lblExchanges)
        #
        # self.setLayout(vboxMarketInfo)

    # tab2
    def initStocks(self, wgtParent):
        print('종목검색')
        lblTitle.setText('종목검색')

    # tab3
    def initSuggests(self, wgtParent):
        print('추천종목')
        lblTitle.setText('추천종목')

    def changeTab(self, nTabIdx):
        self.tabMain.setCurrentIndex(nTabIdx)

    def tabMain_on_changed(self, nTabIdx):
        print('tabMain_on_changed : ' + str(nTabIdx))

        if nTabIdx == 0:
            self.initMarketInfo(tabMain.widget(nTabIdx))

        elif nTabIdx == 1:
            self.initStocks(tabMain.widget(nTabIdx))

        elif nTabIdx == 2:
            self.initSuggests(tabMain.widget(nTabIdx))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    sys.exit(app.exec_())