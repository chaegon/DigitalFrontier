import sys
from PyQt5.QtWidgets import *

import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc


class KOSPI(QWidget):

    def drawChartMarketInfo(self, wgtParent, index, dic):

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        end = datetime.datetime.now()
        start = end + datetime.timedelta(days=-90)

        if index == 'KOSPI':
            target = '^KS11'
            value =  dic["kospi_value"]
        elif index == 'KOSDAQ':
            target = '^KQ11'
            value = dic["kosdaq_value"]

        kospi_df = web.DataReader(target, "yahoo", start, end)

        day_list = []
        name_list = []
        # 'Date' 인덱스를 컬럼으로 변환
        kospi_df.reset_index(inplace=True)

        for i, day in enumerate(kospi_df.Date):
            if day.dayofweek == datetime.datetime.today().weekday():
                day_list.append(i)
                name_list.append(day.strftime('%m-%d'))

        # X축 날짜 표시
        ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

        # 그래프 title과 축 이름 지정
        ax.set_title(index + ' INDEX : ' + value, fontsize=22)
        ax.set_xlabel('Date')

        # 캔들차트 그리기
        candlestick2_ohlc(ax, kospi_df['Open'], kospi_df['High'],
                          kospi_df['Low'], kospi_df['Close'],
                          width=0.5, colorup='r', colordown='b')
        ax.legend()
        ax.grid(True, axis='y', linestyle='--')
        canvas = FigureCanvas(fig)
        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(canvas)
        canvas.draw()


# 단독 실행일 때만 Window 그리기
if __name__ == '__main__':
    app = QApplication(sys.argv)

    thisWindow = KOSPI()
    thisWindow.setWindowTitle("시장현황")
    thisWindow.setGeometry(100, 100, 1400, 920)
    thisWindow.show()

    thisWindow.drawChartMarketInfo(thisWindow, 'KOSPI')

    sys.exit(app.exec_())