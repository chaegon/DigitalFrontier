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

from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from os import path

import matplotlib.pyplot as plt
from matplotlib import rc, font_manager

import platform
# matplotlib 폰트설정
if platform.system() == 'Darwin':  # macOS
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False  # Window 한글 폰트 설정 방법 필요
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ohlc

dbpath = r'./server/DIGITALFRONTIER.db'
dirpath = r'./'
if __name__ == '__main__':
    dbpath = r'./DIGITALFRONTIER.db'
    dirpath = r'../'


# ../data/Stock_Pirce.csv 파일 생성
def create_stock_price(stock_code):
    print('create_stock_price ' + stock_code)

    # 저장파일 경로,명 변경 : data/stock_price/(종목코드).csv
    str_save_file_path = dirpath + 'data/stock_price/'+stock_code+'.csv'
    if path.isfile(str_save_file_path):
        return print('file already exists : ' + str_save_file_path)

    conn = sqlite3.connect(dbpath, isolation_level=None)
    cur = conn.cursor()
    query = '''
        SELECT
              *
          FROM STOCK_PRICE
         WHERE Code = '{stock_code}'         
        '''.format(stock_code=stock_code)

    print(query)

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stock_price_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    if len(stock_price_df) > 0:
        print('(stock_code).csv path : ' + str_save_file_path)
        stock_price_df.to_csv(str_save_file_path, mode='w', index=False)
    else:
        print('No Price Infomation about ' + stock_code)

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (Stock_Price.csv Create)")


# 종목코드값 받아서 차트 그리기
def drawchart_stock(code, wgtParent):
    # 차트 시작 일자 설정 (조회일로 부터 90일 전)
    start = datetime.datetime.now() + datetime.timedelta(days=-90)

    # DB에서 90일치 종목코드에 대한 주가정보 데이터프레임으로 가져오기

    conn = sqlite3.connect(dbpath, isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM STOCK_PRICE WHERE code = '" + code + "' AND Date >= '" + start.strftime('%Y-%m-%d') + "'"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stock_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    stock_df['Date2'] = pd.to_datetime(stock_df['Date'])

    print(stock_df)

    # 차트 그리기
    fig = plt.figure()
    ax = fig.add_subplot(111)

    day_list = []
    name_list = []

    for i, day in enumerate(stock_df['Date2']):
        print('[{}] {}'.format(i, day))
        # if day.dayofweek == datetime.datetime.today().weekday():
        day_list.append(i)
        name_list.append(day.strftime('%m-%d'))

    print(pd.DataFrame([day_list, name_list]))

    # X축 날짜 표시
    ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))
    plt.xticks(rotation=45)

    # 그래프 title과 축 이름 지정
    ax.set_title(stock_df['Name'].unique()[0], fontsize=22)
    # ax.set_xlabel('Date')

    # 캔들차트 그리기
    candlestick2_ohlc(ax, stock_df['Open'], stock_df['High'],
                      stock_df['Low'], stock_df['Close'],
                      width=0.5, colorup='r', colordown='b')
    ax.legend()
    ax.grid(True, axis='x', linestyle='--')
    plt.grid()

    if __name__ == '__main__':
        plt.show()
    else:
        canvas = FigureCanvas(fig)
        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(canvas)
        canvas.draw()

    # 화면 표시

    # canvas = FigureCanvas(fig)
    # vbxIndexes = QVBoxLayout(wgtParent)
    # vbxIndexes.addWidget(canvas)
    # canvas.draw()

    # commit 및 종료
    conn.commit()
    conn.close()

    return


# 종목 예측 차트 그리기
def drawStockPredict(code, wgtParent):
    print('>>> drawStockPredict : {}'.format(code))
    btn_stat_pred = None

    n_stat_pred = getPredictDataStatus(code)
    print('>> Predict Status {}'.format(n_stat_pred))

    if n_stat_pred == 100:
        print('>> Predict Result Ready : ' + code)

    elif 0 < n_stat_pred < 100 :
        str_msg = str('AI 분석 진행중입니다\n{} %'.format(n_stat_pred))
        print('>> Predict Processing: ' + str_msg)
        btn_stat_pred = QPushButton(str_msg, wgtParent)
    else:
        print('>> Predict Status Not Exist')
        str_msg = '예측 정보가 존재하지 않습니다.\n(분석시작)'
        btn_stat_pred = QPushButton(str_msg, wgtParent)

    # if pred data not exist
    if btn_stat_pred is not None:
        print('>> resize predict data not exist')
        btn_stat_pred.move(100,0)
        btn_stat_pred.resize(wgtParent.width(), wgtParent.height())
        btn_stat_pred.setStyleSheet('font: 24px "Malgun Gothic"; font-weight: bold;')
        return

    str_pred_file_path = dirpath + 'data/predict/' + code + '_pred.csv'
    df_pred = pd.read_csv(str_pred_file_path, names=['index','date','price'], header=0)
    df_pred['date']  = df_pred['date'].apply(lambda x: x[5:])
    df_pred['price'] = df_pred['price'].apply(lambda x: int(float(x[1:-1])))
    print(df_pred)

    # 차트 그리기
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('향후예측')

    plt.ylabel('주가')
    plt.xlabel('일자')
    plt.xticks(rotation=45)

    plt.plot(df_pred['date'], df_pred['price'])
    plt.grid()

    if __name__ == '__main__':
        plt.show()
    else:
        canvas = FigureCanvas(fig)
        vbxIndexes = QVBoxLayout(wgtParent)
        vbxIndexes.addWidget(canvas)
        canvas.draw()


def getPredictDataStatus(code):
    print('>>> getPredictDataStatus')

    str_pred_file_path = dirpath + 'data/predict/' + code + '_pred.csv'
    str_learn_stat_file_path = dirpath + 'freezing/' + code + '_learn.ing'

    if path.isfile(str_pred_file_path) is True:
        print('>> Prediction file: ' + str_pred_file_path)
        return 100
    elif path.isfile(str_learn_stat_file_path) is True:
        print('>> Learning file  : ' + str_learn_stat_file_path)
        f = open(str_learn_stat_file_path, 'r')
        str_learn_stat = f.read()
        print('>> Learning Status: ' + str_learn_stat)
        f.close()
        return int(str_learn_stat)

    return 0


def change_name_to_code(name):
    conn = sqlite3.connect(dbpath, isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM CODE_DATA WHERE name = '"+name+"'"

    result = cur.execute(query)
    code = result.fetchone()[2]

    # commit 및 종료
    conn.commit()
    conn.close()

    return code


# 실시간 종목코드별 금액 정보 가져오기
# 파라미터(code): 종목코드  ex) 삼성전자:005390
# return : 종목코드, 종목명, 현재가, 변동가, 변동률, 등
def get_stock_realtime_info(code):
    url = "https://finance.naver.com/item/main.nhn?code="+code
    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser")

    name = html.find("title").string.split(':')[0].strip()
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
        , "name": name
        , "today_price": today_price
        , "today_change": today_change
        , "today_change_pc": today_change_pc
        , "updown": updown
    }
    return stock_realtime_info


# 차트그리기를 위한 지수별 금액정보 데이터프레임 반환
# 파라미터(index_name): KOSPI, KOSDAQ, KPI200
def get_main_info_chart(index_name):
    conn = sqlite3.connect(dbpath, isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM DAILY_"+index_name+"_INDEX"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    index_df = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)

    # commit 및 종료
    conn.commit()
    conn.close()

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
