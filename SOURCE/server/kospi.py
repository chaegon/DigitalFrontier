import sys
from PyQt5.QtWidgets import *

import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc


class KOSPI(QWidget):

    def drawChartMarketInfo(self, wgtParent):
        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        start = datetime.datetime(2020, 10, 1)
        end = datetime.datetime.now()
        kospi_df = web.DataReader("^KS11", "yahoo", start, end)
        # index = kospi_df.index.astype('str')  # 캔들스틱 x축이 str로 들어감

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
        vbxIndexes.addWidget(canvas)
        canvas.draw()


# 단독 실행일 때만 Window 그리기
if __name__ == '__main__':
    app = QApplication(sys.argv)

    thisWindow = KOSPI()
    thisWindow.setWindowTitle("시장현황")
    thisWindow.setGeometry(100, 100, 1400, 920)
    thisWindow.show()

    thisWindow.drawChartMarketInfo(thisWindow)

    sys.exit(app.exec_())