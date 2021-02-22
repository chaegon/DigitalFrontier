import os
from sys import exit as sysExit
import pandas as pd

from PyQt5.QtWidgets import QWidget, QLabel

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
    from server_main import get_stock_realtime_info
else:
    from .server_main import get_stock_realtime_info


# find stock code  종목명 -> 코드목록 검색
def getDataCodeName(sKeyword):
    sKeyword = sKeyword.strip().upper()
    print('>> 검색어 [' + sKeyword + ']')
    # print(df_code_name.columns)

    list_search = []
    for idx, row in df_code_name[['code', 'name']].iterrows():
        for content in row:
            if sKeyword in content:
                # print(idx)
                list_search.append(df_code_name.loc[idx])
                break

    df_search = pd.DataFrame(list_search, columns=df_code_name.columns).reset_index()
    print(df_search[['type', 'code', 'name']])
    print('--------------------------------------\n')

    return df_search


def runOnTerminal():
    while True:
        sKeyword = input('검색어를 입력하세요(exit=종료): ')
        if sKeyword == 'exit': break
        df_find = getDataCodeName(sKeyword)

        sStockCode = str(input('종목코드를 입력하세요: '))
        dict_info = get_stock_realtime_info(sStockCode)
        df_stock_info_list = pd.DataFrame([dict_info])
        # code:종목코드 today_price:현재가 today_change:전일대비 today_change_pc:전일대비 updown:등락
        print(df_stock_info_list)
        print('======================================\n')


class UIWidget(QWidget):
    def init(self):
        self.setWindowTitle("종목 검색 및 현황")
        self.setGeometry(100, 100, 800, 600)

        grid = QGridLayout()

        fldKeyword = QLineEdit(self)
        fldKeyword.setObjectName('keyword')
        grid.addWidget(fldKeyword,0,0)
        # fldKeyword.move(60, 20)
        # fldKeyword.textChanged[str].connect(self.fldKeyword_on_changed)

        btnSearch = QPushButton('종목검색', self)
        grid.addWidget(btnSearch,0,1)
        # btnSearch.move(240, 20)
        btnSearch.clicked.connect(self.btnSearch_on_clicked)

        gboxStockInfoList = QGroupBox('종목검색결과')
        gboxStockInfoList.setObjectName('gboxStockInfoList')
        grid.addWidget(gboxStockInfoList,1,0)

        self.setLayout(grid)
        thisWindow.show()

    # draw stock information line from dataframe on target widget (not chart)
    def drawStockInfo(self, dict_stock_info):
        print('drawStockInfo')
        print(dict_stock_info)

        hbox = QHBoxLayout()
        for key, value in dict_stock_info.items():
            hbox.addWidget(QLabel(value))
        # wgtParent.setLayout(hbox)
        return hbox

    def btnSearch_on_clicked(self, checked):
        print('1')
        gbox = self.findChild(QGroupBox, 'gboxStockInfoList')
        print('2')

        # find vbox previous defined
        vbox = self.findChild(QVBoxLayout, 'vboxStockInfoList')
        if vbox is None:
            # init vbox
            vbox = QVBoxLayout()
            vbox.setObjectName('vboxStockInfoList')
        else:
            # delete child widgets
            for i in reversed(range(vbox.count())):
                vbox.itemAt(i).widget().deleteLater()

        fldKeyword = self.findChild(QLineEdit, 'keyword')
        sKeyword = fldKeyword.text()
        df_code_list = getDataCodeName(sKeyword)
        for code in df_code_list['code']:
            print(code)
            dict_stock_info = get_stock_realtime_info(code)
            # df_stock_info = pd.DataFrame([dict_stock_info])
            # print(dict_stock_info)
            hbox = self.drawStockInfo(dict_stock_info)
            wgt_new_stock_info = QWidget()
            wgt_new_stock_info.setLayout(hbox)
            vbox.addWidget(wgt_new_stock_info)
        gbox.setLayout(vbox)

    def keyPressEvent(self, e):
        # print("event", e)
        # super(UIWidget, self).keyPressEvent(e)
        if e.key() == 16777220:
            print(' enter')

# END DEFINITION


# change work directory
print(os.getcwd())
if __name__ == '__main__':
    os.chdir(os.path.abspath('../'))
    print(os.getcwd())

print('initialize code list data')
df_code_name = pd.read_csv('./data/code-name.csv', dtype={'code':str})


# Run as Stand-alone
if __name__ == '__main__':

    if(False):
        runOnTerminal()
    else:
        app = QApplication([])
        thisWindow = UIWidget()
        thisWindow.init()
        sysExit(app.exec_())
