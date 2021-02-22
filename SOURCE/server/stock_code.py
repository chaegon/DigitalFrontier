import os
from sys import exit as sysExit
import pandas as pd

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGroupBox

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
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


# draw stock information line from dataframe on target widget (not chart)
def drawStockInfo(dict_stock_info, wgtParent):
    print('drawStockInfo')
    print(dict_stock_info)

    wgtThisStockInfo = QWidget()

    textCode = QLabel(dict_stock_info['code'], wgtThisStockInfo)

    wgtParent.addWidget(wgtThisStockInfo)


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

        fldKeyword = QLineEdit(thisWindow)
        fldKeyword.move(60, 20)
        fldKeyword.keyPressEvent = self.keyPressEvent

        thisWindow.show()

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
