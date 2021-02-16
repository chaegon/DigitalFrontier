import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import io
import zipfile
import xml.etree.ElementTree as et
import json
import FinanceDataReader as fdr
import sqlite3
import pandas_datareader.data as web
import pandas as pd

import load_db
import matplotlib.pyplot as plt
from matplotlib import rc
# matplotlib 폰트설정
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False # Window 한글 폰트 설정 방법 필요

import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ohlc

def create_stock_price():
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM STOCK_PRICE"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stock_price_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    stock_price_df.to_csv('Stock_Price222.csv', mode='w', inedx = None)


# 종목코드값 받아서 차트 그리기
def drawchart_stock(code):

    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM STOCK_PRICE WHERE code = '" + code + "'"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stock_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)

    # 3. 캔들차트
    fig = plt.figure(figsize=(20, 10))
    index = stock_df['Date'].astype('str')  # 캔들스틱 x축이 str로 들어감
    ax = fig.add_subplot(111)

    # X축 티커 숫자 20개로 제한
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

    # 그래프 title과 축 이름 지정
    ax.set_title(stock_df['Name'].unique()[0], fontsize=22)
    ax.set_xlabel('Date')

    # 캔들차트 그리기
    candlestick2_ohlc(ax, stock_df['Open'], stock_df['High'],
                      stock_df['Low'], stock_df['Close'],
                      width=0.5, colorup='r', colordown='b')
    ax.legend()
    plt.grid()
    plt.show()


def change_name_to_code(name):
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM CODE_DATA WHERE name = '"+name+"'"

    result = cur.execute(query)
    code = result.fetchone()[2]

    return code


# 실시간 종목코드별 금액 정보 가져오기
# 파라미터(code): 종목코드  ex) 삼성전자:005390
def get_stock_realtime_info(code):
    url = "https://finance.naver.com/item/main.nhn?code="+code
    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser")

    today_price = html.find("p", {"class": "no_today"}).find("span", {"class": "blind"}).string
    today_change = html.find("p", {"class": "no_exday"}).find("span", {"class": "blind"}).string
    today_change_pc = html.find("p", {"class": "no_exday"}).find_all("span", {"class": "blind"})[1].string
    exday_price = html.find("td", {"class": "first"}).find("span", {"class": "blind"}).string
    if today_price > exday_price:
        updown = 'up'
    else:
        updown = 'down'

    stock_realtime_info = {
        "code": code
        , "today_price": today_price
        , "today_change": today_change
        , "today_change_pc": today_change_pc
        , "updown": updown
    }
    return stock_realtime_info

# 차트그리기를 위한 지수별 금액정보 데이터프레임 반환
# 파라미터(index_name): KOSPI, KOSDAQ, KPI200
def get_main_info_chart(index_name):
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM DAILY_"+index_name+"_INDEX"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    index_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)

    # 차트그리기 ==> Chart.py 참조
    return index_df

# 실시간 환율정보 가져오기
# 데이터 타입: Dictionary
# 예시: exhcange_info[0][0]: 미국 USD / exhcange_info[0][1]: 1,103.5 / exhcange_info[0][2]: 7.50 / exhcange_info[0][3]: 상승
def get_main_info_exchange():
    exchange_info = {}
    url = "https://finance.naver.com/marketindex/"
    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser", from_encoding='euc-kr')
    currency_name = html.select("h3.h_lst > span.blind")
    currency_value = html.select("span.value")
    currency_change = html.select("span.change")
    currency_temp = html.select("span.blind")

    for i in range(0, 4):
        exchange_info[i] = [currency_name[i].string, currency_value[i].string, currency_change[i].string, currency_temp[i + 2].string]

    return exchange_info


# 실시간 주가지수정보 가져오기
# 데이터 타입: Dictionary
# 예시: index_info["kospi_value"] ==> 실시간 코스피 지수
def get_main_info_index():
    url = "https://finance.naver.com/sise/"
    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser")

    index_info = {"kospi_value": html.find("span", {"class": "num", "id": "KOSPI_now"}).string
        , "kospi_change": html.find("span", {"class": "num_s", "id": "KOSPI_change"}).text.split(' ')[0]
        , "kospi_changepc": html.find("span", {"class": "num_s", "id": "KOSPI_change"}).text.split(' ')[1].split('%')[0]

        , "kosdaq_value": html.find("span", {"class": "num", "id": "KOSDAQ_now"}).string
        , "kosdaq_change": html.find("span", {"class": "num_s", "id": "KOSDAQ_change"}).text.split(' ')[0]
        , "kosdaq_changepc": html.find("span", {"class": "num_s", "id": "KOSDAQ_change"}).text.split(' ')[1].split('%')[0]

        , "kpi200_value": html.find("span", {"class": "num", "id": "KPI200_now"}).string
        , "kpi200_change": html.find("span", {"class": "num_s", "id": "KPI200_change"}).text.split(' ')[0]
        , "kpi200_changepc": html.find("span", {"class": "num_s", "id": "KPI200_change"}).text.split(' ')[1].split('%')[0]
                  }

    return index_info

# 네이버 증권 url 업종별 종목코드 가져오기
def get_stocks(url):
    stocks = pd.DataFrame()
    stock_codes = []
    stock_names = []

    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser")

    tr_list = html.find_all("tr", {"onmouseover": "mouseOver(this)"})
    for tr in tr_list:
        alist = tr.find_all("a")[0]
        code = str(alist["href"])[-6:]
        name = str(alist.string)

        stock_codes.append(code)
        stock_names.append(name)

    stocks['name'] = stock_names
    stocks['code'] = stock_codes

    return stocks

# 종목코드에 대한 기간별 가격정보 가져오기
def get_stocks_price(stocks,starts_date,end_date):
    stock_price = pd.DataFrame()

    price = pd.DataFrame()
    for code, name in zip(stocks['code'], stocks['name']):
        price = fdr.DataReader(code, starts_date, end_date)
        price['Code'] = code
        price['Name'] = name

        price.reset_index(inplace=True)
        stock_price = pd.concat([stock_price, price], axis=0, ignore_index=True)

    stock_price = stock_price[["Name", "Code", "Date", "Open", "High", "Low", "Close", "Volume", "Change"]]
    stock_price['Name'] = pd.Series(stock_price['Name'], dtype="string")
    stock_price['Code'] = pd.Series(stock_price['Code'], dtype="string")
    stock_price['Code'] = stock_price['Code'].str.zfill(6)
    stock_price.set_index('Code', inplace=True)

    return stock_price

def get_corpcode(crtfc_key):
    """ OpenDART 기업 고유번호 받아오기 return 값: 주식코드를 가진 업체의 DataFrame """
    params = {'crtfc_key':crtfc_key}
    items = ["corp_code","corp_name","stock_code","modify_date"]
    item_names = ["고유번호","회사명","종목코드","수정일"]
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    res = requests.get(url,params=params)
    zfile = zipfile.ZipFile(io.BytesIO(res.content))
    fin = zfile.open(zfile.namelist()[0])
    root = et.fromstring(fin.read().decode('utf-8'))
    data = []
    for child in root:
        if len(child.find('stock_code').text.strip()) > 1:
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    df = pd.DataFrame(data, columns=item_names)
    return df


def convertFnltt(url, items, item_names, params):
    res = requests.get(url, params)
    json_dict = json.loads(res.text)
    data = []
    if json_dict['status'] == "000":
        for line in json_dict['list']:
            data.append([])
            for itm in items:
                if itm in line.keys():
                    data[-1].append(line[itm])
                else:
                    data[-1].append('')
    df = pd.DataFrame(data, columns=item_names)
    return df


# 단일회사 주요계정
def get_fnlttSinglAcnt(crtfc_key, corp_code, bsns_year, reprt_code):
    items = ["rcept_no", "bsns_year", "stock_code", "reprt_code", "account_nm", "fs_div", "fs_nm",
             "sj_div", "sj_nm", "thstrm_nm", "thstrm_dt", "thstrm_amount", "thstrm_add_amount",
             "frmtrm_nm", "frmtrm_dt", "frmtrm_amount","frmtrm_add_amount", "bfefrmtrm_nm",
             "bfefrmtrm_dt", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호", "사업연도", "종목코드", "보고서코드", "계정명", "개별연결구분",
                  "개별연결명", "재무제표구분", "재무제표명", "당기명", "당기일자","당기금액",
                  "당기누적금액", "전기명", "전기일자", "전기금액","전기누적금액", "전전기명",
                  "전전기일자", "전전기금액", "계정과목정렬순서"]
    params = {'crtfc_key':crtfc_key, 'corp_code':corp_code, 'bsns_year':bsns_year,'reprt_code':reprt_code}
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
    return convertFnltt(url,items,item_names,params)


# 단일회사 전체 재무제표
def get_fnlttSinglAcntAll(crtfc_key, corp_code, bsns_year, reprt_code, fs_div = "CFS"):
    items = ["rcept_no","reprt_code","bsns_year","corp_code","sj_div","sj_nm", "account_id",
             "account_nm","account_detail","thstrm_nm", "thstrm_amount","thstrm_add_amount",
             "frmtrm_nm","frmtrm_amount", "frmtrm_q_nm","frmtrm_q_amount","frmtrm_add_amount",
             "bfefrmtrm_nm", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호","보고서코드","사업연도","고유번호","재무제표구분", "재무제표명","계정ID","계정명",
                  "계정상세","당기명","당기금액", "당기누적금액","전기명","전기금액","전기명(분/반기)",
                  "전기금액(분/반기)","전기누적금액","전전기명","전전기금액", "계정과목정렬순서"]
    params = {'crtfc_key':crtfc_key, 'corp_code':corp_code, 'bsns_year':bsns_year, 'reprt_code':reprt_code, 'fs_div':fs_div}
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    return convertFnltt(url,items,item_names,params)

# 다중회사 주요계정
def get_fnlttMultiAcnt(crtfc_key, corp_code, bsns_year, reprt_code):
    items = ["rcept_no", "bsns_year", "stock_code", "reprt_code", "account_nm", "fs_div", "fs_nm",
             "sj_div", "sj_nm", "thstrm_nm", "thstrm_dt", "thstrm_amount","thstrm_add_amount",
             "frmtrm_nm", "frmtrm_dt", "frmtrm_amount","frmtrm_add_amount", "bfefrmtrm_nm",
             "bfefrmtrm_dt", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호", "사업연도", "종목코드", "보고서코드", "계정명", "개별연결구분","개별연결명", "재무제표구분",
                  "재무제표명", "당기명", "당기일자","당기금액", "당기누적금액", "전기명", "전기일자", "전기금액",
                  "전기누적금액", "전전기명", "전전기일자", "전전기금액", "계정과목정렬순서"]
    corps_str = ",".join(corp_code)
    params = {'crtfc_key':crtfc_key, 'corp_code':corps_str, 'bsns_year':bsns_year,'reprt_code':reprt_code}
    url = "https://opendart.fss.or.kr/api/fnlttMultiAcnt.json"
    return convertFnltt(url,items,item_names,params)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_stock_price()