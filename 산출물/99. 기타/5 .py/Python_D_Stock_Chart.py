# 2020.12.28 이상효 - Yahoo에서 일봉 데이터 받아 차트 그리기

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import mplfinance
from mplfinance.original_flavor import candlestick_ohlc


start = datetime.datetime(2020,12,1)
end = datetime.datetime(2020,12,27)
samsung = web.DataReader("005930.KS", "yahoo",start,end)

samsung.info()

# 선차트
#plt.plot(samsung.index, samsung['Adj Close'])
#plt.show()

# 캔들차트
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
mplfinance.plot(samsung,type='candle')

candlestick_ohlc(ax, samsung['Open'], samsung['High'], samsung['Low'], samsung['Close'], width=0.2, colorup='r', colordown='b', alpha=1.0)
