import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QCursor
# from PyQt5.QtCore import QRect
# from PyQt5 import uic

from server import stock_code
from server import kospi
from server import server_main

# import pandas as pd
from functools import partial


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
        tab3 = QWidget()

        tab1.setObjectName('tab1')
        tab2.setObjectName('tab2')
        tab3.setObjectName('tab3')

        tabMain = QTabWidget()
        tabMain.setObjectName('tabMain')
        tabMain.setTabPosition(QTabWidget.North)

        tabMain.addTab(tab1, '시장현황')
        tabMain.addTab(tab2, '종목검색')
        tabMain.addTab(tab3, '종목현황')
        tabMain.currentChanged.connect(self.tabMain_on_changed)

        vboxMain = QVBoxLayout()
        vboxMain.addWidget(lblTitle)
        vboxMain.addWidget(tabMain)
        self.setLayout(vboxMain)

        lblTitle.setText('시장현황')
        self.initMarketInfo(tab1)
        self.initStocks(tab2)
        self.initSuggests(tab3)

        self.setWindowTitle('판타스틱4')
        self.setGeometry(10, 50, 1000, 980)
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
        print('종목검색')
        grid = QGridLayout()

        fldKeyword = QLineEdit(wgtParent)
        fldKeyword.setObjectName('keyword')
        grid.addWidget(fldKeyword,0,0)
        # fldKeyword.move(60, 20)
        # fldKeyword.textChanged[str].connect(self.fldKeyword_on_changed)

        btnSearch = QPushButton('검색', wgtParent)
        grid.addWidget(btnSearch,0,1)
        # btnSearch.move(240, 20)
        btnSearch.clicked.connect(self.btnSearch_on_clicked)

        gboxStockInfoList = QGroupBox('종목검색결과')
        gboxStockInfoList.setObjectName('gboxStockInfoList')
        grid.addWidget(gboxStockInfoList,1,0)

        wgtParent.setLayout(grid)

    # draw stock information line from dataframe on target widget (not chart)
    def drawStockInfoButton (self, dict_stock_info, wgtParent):
        print(dict_stock_info)

        style = 'font: 16px "Malgun Gothic";'
        style_debug = ''  # 'background-color: #87CEFA;'

        updown = '- '
        updown_pc = ' '
        style_color = 'color: black;'
        if dict_stock_info['updown'] == 'up':
            updown = '▲ '
            updown_pc = '+ '
            style_color = 'color: red;'
        elif dict_stock_info['updown'] == 'down':
            updown = '▼ '
            updown_pc = '- '
            style_color = 'color: blue;'

        hbox = QHBoxLayout()

        lblCode = QLabel(dict_stock_info['code'])
        lblCode.setFixedWidth(80)
        lblCode.setStyleSheet(style_debug + style + 'padding-left: 20;')
        hbox.addWidget(lblCode)

        lblName = QLabel(dict_stock_info['name'])
        lblName.setFixedWidth(240)
        lblName.setStyleSheet(style_debug + 'font: 24px "Malgun Gothic"; font-weight: bold;')
        hbox.addWidget(lblName)

        lblPrice = QLabel(dict_stock_info['today_price'])
        lblPrice.setFixedWidth(200)
        lblPrice.setStyleSheet(style_debug + 'font: 24px "Malgun Gothic";' + style_color)
        lblPrice.setAlignment(QtCore.Qt.AlignRight)
        hbox.addWidget(lblPrice)

        # lblUpDown = QLabel(updown)
        # lblUpDown.setFixedWidth(20)
        # lblUpDown.setStyleSheet(style_debug + style + style_color)
        # lblUpDown.setAlignment(QtCore.Qt.AlignRight)
        # hbox.addWidget(lblUpDown)

        str_today_change = updown + dict_stock_info['today_change']  # + '   ' + updown_pc + dict_stock_info['today_change_pc']+' %'
        lblChange = QLabel(str_today_change)
        lblChange.setFixedWidth(160)
        lblChange.setStyleSheet(style_debug + 'font: 18px "Malgun Gothic";' + style_color)
        lblChange.setAlignment(QtCore.Qt.AlignRight)
        hbox.addWidget(lblChange)

        lblChangePer = QLabel(updown_pc + dict_stock_info['today_change_pc']+' %')
        lblChangePer.setFixedWidth(100)
        lblChangePer.setStyleSheet(style_debug + style + style_color)
        lblChangePer.setAlignment(QtCore.Qt.AlignRight)
        hbox.addWidget(lblChangePer)

        wgtParent.setLayout(hbox)
        wgtParent.setFixedHeight(80)
        return hbox

    # stock info click event
    def stock_info_on_click (self, code):
        # create price csv file
        # server_main.create_stock_price(code)
        # self.changeTab(2)
        self.drawStockInfoSheet(code)

    # def fldKeyword_on_changed(self, sKeyword):
    def btnSearch_on_clicked(self, checked):
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

        # for code in df_code_list['code']:
        n_max_result = 10
        for idx in range(0,n_max_result):  # count of button to create include empty
            wgt_new_stock_info = QPushButton()
            wgt_new_stock_info.setFixedHeight(80)

            if idx < len(df_code_list['code']):
                code = df_code_list['code'][idx]
                print(code)
                dict_stock_info = server_main.get_stock_realtime_info(code)
                # df_stock_info = pd.DataFrame([dict_stock_info])
                # print(dict_stock_info)
                self.drawStockInfoButton(dict_stock_info, wgt_new_stock_info)
                # button clicked signal should set 'code' parameter each button
                wgt_new_stock_info.clicked.connect(partial(self.stock_info_on_click, code))
                wgt_new_stock_info.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            vbox.addWidget(wgt_new_stock_info)

        str_result_msg = '검색이 완료되었습니다.'
        if len(df_code_list['code']) > n_max_result:
            str_result_msg = '검색 결과는 최대 10개까지만 표시됩니다.'
        lblCodeListMore = QLabel(str_result_msg)
        vbox.addWidget(lblCodeListMore)

        gbox = self.findChild(QGroupBox, 'gboxStockInfoList')
        gbox.setLayout(vbox)
        print('\n>> end draw stock info list\n')

    # tab3
    def initSuggests(self, wgtParent):
        print('종목현황')

        self.drawStockInfoSheet('')

        # lblAIintro = QLabel('종목 검색 후 선택하세요', wgtParent)
        # # lblAIintro = QLabel('AI가 추천하는 투자 종목', wgtParent)
        # fntAIintro = lblAIintro.font()
        # fntAIintro.setPointSize(16)
        # lblAIintro.setFont(fntAIintro)
        # lblAIintro.move(10,10)

        ### test
        # self.changeTab(2)
        # self.drawStockInfoSheet('195870')

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

    # blah
    def drawStockInfoSheet(self, code):
        print('>> drawStockInfoSheet ' + code)

        tab3 = self.findChild(QWidget, 'tab3')
        vbox = self.findChild(QVBoxLayout, 'vboxStockInfoSheet')
        if vbox is None:
            # init vbox
            vbox = QVBoxLayout()
            vbox.setObjectName('vboxStockInfoSheet')
        else:
            # delete child widgets
            for i in reversed(range(vbox.count())):
                # vbox.itemAt(i).widget().deleteLater()
                vbox.itemAt(i).widget().setParent(None)

        if code == '':
            lblAIintro = QLabel('종목 검색 후 선택하세요')
            fntAIintro = lblAIintro.font()
            fntAIintro.setPointSize(16)
            lblAIintro.setFont(fntAIintro)
            vbox.addWidget(lblAIintro, alignment=QtCore.Qt.AlignTop)
            tab3.setLayout(vbox)
            return

        dict_stock_info = server_main.get_stock_realtime_info(code)
        print(dict_stock_info)

        # 종목
        wgtStockInfo = QWidget()
        self.drawStockInfoButton(dict_stock_info, wgtStockInfo)

        # 종목차트
        wgtStockChart = QWidget()
        wgtStockChart.setFixedHeight(400)
        server_main.drawchart_stock(code, wgtStockChart)

        # 향후 예측
        wgtStockPredict = QWidget()
        wgtStockPredict.setFixedHeight(400)
        server_main.drawStockPredict(code, wgtStockPredict)

        vbox.addWidget(wgtStockInfo)
        vbox.addWidget(wgtStockChart)
        vbox.addWidget(wgtStockPredict)

        tab3.setLayout(vbox)

    # resize image
    def getCroppedPixmap(self, sImagePath):
        imgTarget = QImage(sImagePath)
        imgCropped = imgTarget.copy(100, 20, 1300, 520)
        return QPixmap(imgCropped)

    def changeTab(self, nTabIdx):
        tabMain = self.findChild(QTabWidget, 'tabMain')
        tabMain.setCurrentIndex(nTabIdx)

    def tabMain_on_changed(self, nTabIdx):
        tabMain = self.findChild(QTabWidget, 'tabMain')
        sTabName = tabMain.tabText(nTabIdx)

        # self.findChild(QTabWidget, 'tabMain')
        # if nTabIdx == 0:
            # self.initMarketInfo(tabMain.widget(nTabIdx))
            # sTabName = '시장현황'
        # elif nTabIdx == 1:
            # self.initStocks(tabMain.widget(nTabIdx))
            # sTabName = '종목검색'
        # elif nTabIdx == 2:
            # self.initSuggests(tabMain.widget(nTabIdx))
            # sTabName = '종목현황'

        lblTitle = self.findChild(QLabel, 'currentTitle')
        lblTitle.setText(sTabName)
        print('tabMain_on_changed ['+str(nTabIdx)+'] ' + sTabName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Fantastic4()
    sys.exit(app.exec_())