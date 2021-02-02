import pandas as pd
import pandas_datareader.data as web
import datetime
import FinanceDataReader as fdr

from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

# 1. 지수 정보 수집
start = datetime.datetime(2020,10,1)
end = datetime.datetime.now()

kospi_df = web.DataReader("^KS11", "yahoo",start,end)
kosdaq_df = web.DataReader("^KQ11", "yahoo",start,end)
kpi200_df = fdr.DataReader('KS200',start,end) #코스피200의 경우 fdr.Datareader에서 가져옴


# 2. 선차트 그리기
fig, ax = plt.subplots(figsize=(10,5))

ax.set_title('KOSPI INDEX', fontsize=15)
ax.set_ylabel("KOSPI")
ax.set_xlabel("Date Time")
ax.plot(kospi_df.index, kospi_df[['Close']])
ax.legend(['Close'])
plt.show()


# 3. 캔들차트
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
index = kospi_df.index.astype('str') # 캔들스틱 x축이 str로 들어감

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
plt.grid()
plt.show()
