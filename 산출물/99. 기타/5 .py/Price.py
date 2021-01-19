import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import FinanceDataReader as fdr

stocks_semiconductor = pd.DataFrame()
stock_price = pd.DataFrame()
stock_codes = []
stock_names = []

url = "https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=202"
result = requests.get(url)
html = BeautifulSoup(result.content, "html.parser")

tr_list = html.find_all("tr",{"onmouseover":"mouseOver(this)"})
for tr in tr_list:
    alist = tr.find_all("a")[0]
    code = str(alist["href"])[-6:]
    name = str(alist.string)

    stock_codes.append(code)
    stock_names.append(name)

stocks_semiconductor['name'] = stock_names
stocks_semiconductor['code'] = stock_codes

price = pd.DataFrame()
for code,name in zip(stocks_semiconductor['code'],stocks_semiconductor['name']):
    price = fdr.DataReader(code,'2019-01-01','2020-12-31')
    price['Code'] = code
    price['Name'] = name

    price.reset_index(inplace=True)
    stock_price = pd.concat([stock_price, price], axis=0, ignore_index=True)

stock_price = stock_price[["Name","Code","Date","Open","High","Low","Close","Volume","Change"]]
stock_price['Name'] = pd.Series(stock_price['Name'], dtype="string")
stock_price['Code'] = pd.Series(stock_price['Code'], dtype="string")
stock_price['Code'] = stock_price['Code'].str.zfill(6)
stock_price.set_index('Code',inplace=True)

stock_price.to_csv('Stock_Price.csv',encoding='utf-8-sig')

print(stock_price.head(5))
print(stock_price.tail(5))
