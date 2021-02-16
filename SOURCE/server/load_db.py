import sqlite3
import pandas as pd
import pandas_datareader.data as web
import datetime
import FinanceDataReader as fdr

# sqlite3 설치 필요
# sqlite3 설치 및 설정: https://somjang.tistory.com/entry/SQLite3-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0
# sqlite db browser 설치: https://sqlitebrowser.org/

def index_load_initial():
    # 1. 초기적재
    #    - 2014-01-01 ~ 현재일자 까지 코스피, 코스닥, 코스피200의 일별지수를 테이블에 적재한다.
    #      > 코스닥의 경우 2013년 3월 4일 데이터부터 제공 됨.

    start = datetime.datetime(2014,1,1)
    end = datetime.datetime.now()

    # 지수별 데이터프레임 생성 및 가져오기
    kospi_df = web.DataReader("^KS11", "yahoo",start,end)
    kosdaq_df = web.DataReader("^KQ11", "yahoo", start, end)
    kpi200_df = fdr.DataReader('KS200', start, end)

    kospi_df.drop("Adj Close", axis=1, inplace=True)
    kosdaq_df.drop("Adj Close", axis=1, inplace=True)
    kpi200_df.drop("Change", axis=1, inplace=True)

    kospi_df.reset_index(inplace=True)
    kosdaq_df.reset_index(inplace=True)
    kpi200_df.reset_index(inplace=True)

    kpi200_df = kpi200_df[['Date', 'High', 'Low', 'Open', 'Close', 'Volume']]

    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)

    # 테이블 CREATE 및 INSERT
    kospi_df.to_sql('DAILY_KOSPI_INDEX', conn)
    kosdaq_df.to_sql('DAILY_KOSDAQ_INDEX', conn)
    kpi200_df.to_sql('DAILY_KPI200_INDEX', conn)

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (index_load_initial)")


def index_load_daily():
    # 2. 추가적재
    #  - 마지막 적재 일로 부터 오늘날짜까지 적재
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    max_date_query = cur.execute("SELECT MAX(Date) From DAILY_KOSPI_INDEX")
    max_date = max_date_query.fetchone()
    start = datetime.datetime(int(max_date[0][0:4]), int(max_date[0][5:7]), int(max_date[0][8:10]))
    end = datetime.datetime.now()

    # 지수별 데이터프레임 생성 및 가져오기
    kospi_df = web.DataReader("^KS11", "yahoo", start, end)
    kosdaq_df = web.DataReader("^KQ11", "yahoo", start, end)
    kpi200_df = fdr.DataReader('KS200', start, end)
    kospi_df.reset_index(inplace=True)
    kosdaq_df.reset_index(inplace=True)
    kpi200_df.reset_index(inplace=True)

    kospi_df.drop("Adj Close", axis=1, inplace=True)
    kosdaq_df.drop("Adj Close", axis=1, inplace=True)
    kpi200_df.drop("Change", axis=1, inplace=True)

    if kospi_df['Date'].max() == start:
        return print("No Updates (index_load_daily)")
    else:
        # 테이블 INSERT
        kospi_df.to_sql('DAILY_KOSPI_INDEX', conn, if_exists='append')
        kosdaq_df.to_sql('DAILY_KOSDAQ_INDEX', conn, if_exists='append')
        kpi200_df.to_sql('DAILY_KPI200_INDEX', conn, if_exists='append')

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (index_load_daily)")



def stock_load_all():
    # 3. 코스피, 코스닥 전체 종목코드 적재

    # 한국거래소 홈페이지 크롤링이 막혔기 때문에 csv 파일 업로드로 대체 (2021-01-24)
    # csv 다운로드 : http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020501
    # 3-1. 전체 코스피 종목 정보 csv파일 load
    kospi_all_stocks_df = pd.read_csv("kospi_data_20210124.csv", dtype={'종목코드': 'str'}, encoding='euc-kr')
    kospi_code_data = kospi_all_stocks_df[['종목코드', '종목명']]
    kospi_code_data.columns = ['code', 'name']
    kospi_code_data.insert(0, "type", "KOSPI", True)

    # 3-2. 전체 코스닥 종목 정보 csv파일 load
    kosdaq_all_stocks_df = pd.read_csv("kosdaq_data_20210124.csv", dtype={'종목코드': 'str'}, encoding='CP949')
    kosdaq_code_data = kosdaq_all_stocks_df[['종목코드', '종목명']]
    kosdaq_code_data.columns = ['code', 'name']
    kosdaq_code_data.insert(0, "type", "KOSDAQ", True)

    code_data = pd.concat([kospi_code_data, kosdaq_code_data], ignore_index=True)

    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)

    # 테이블 CREATE 및 INSERT
    code_data.to_sql('CODE_DATA', conn)

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (stock_load_all)")

def stock_price_load_initial():
    # 4. 전체 종목 가격정보 초기 적재

    # 전체 종목코드 정보 가져오기
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM CODE_DATA"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stocks = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    stock_price = pd.DataFrame()

    # 추출 기간 선택 (2020-05-01 ~ 오늘)
    start = datetime.datetime(2020, 5, 1)
    end = datetime.datetime.now()


    # 종목별 가격정보 추출
    for code, name in zip(stocks['code'], stocks['name']):
        price = fdr.DataReader(code, start, end)
        price['Code'] = code
        price['Name'] = name

        price.reset_index(inplace=True)
        stock_price = pd.concat([stock_price, price], axis=0, ignore_index=True)

    stock_price = stock_price[["Name", "Code", "Date", "Open", "High", "Low", "Close", "Volume", "Change"]]
    stock_price['Name'] = pd.Series(stock_price['Name'], dtype="string")
    stock_price['Code'] = pd.Series(stock_price['Code'], dtype="string")
    stock_price['Code'] = stock_price['Code'].str.zfill(6)
    stock_price.set_index('Code', inplace=True)

    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)

    # 테이블 CREATE 및 INSERT
    stock_price.to_sql('STOCK_PRICE', conn)

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (stock_price_load_initial)")

def stock_price_load_daily():
    # 5. 전체종목 가격적재 추가 적재
    #  - 마지막 적재 일로 부터 오늘날짜까지 적재

    # 전체 종목코드 정보 가져오기
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    query = "SELECT * FROM CODE_DATA"

    result = cur.execute(query)
    cols = [column[0] for column in result.description]

    stocks = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    stock_price = pd.DataFrame()

    # commit 및 종료
    conn.commit()
    conn.close()

    # 마지막 적재 날짜 가져오기
    conn = sqlite3.connect("DIGITALFRONTIER.db", isolation_level=None)
    cur = conn.cursor()
    max_date_query = cur.execute("SELECT MAX(Date) From STOCK_PRICE")
    max_date = max_date_query.fetchone()
    start = datetime.datetime(int(max_date[0][0:4]), int(max_date[0][5:7]), int(max_date[0][8:10]))
    end = datetime.datetime.now()

    # 종목별 가격정보 추출
    for code, name in zip(stocks['code'], stocks['name']):
        price = fdr.DataReader(code, start, end)
        price['Code'] = code
        price['Name'] = name

        price.reset_index(inplace=True)
        stock_price = pd.concat([stock_price, price], axis=0, ignore_index=True)

    stock_price = stock_price[["Name", "Code", "Date", "Open", "High", "Low", "Close", "Volume", "Change"]]
    stock_price['Name'] = pd.Series(stock_price['Name'], dtype="string")
    stock_price['Code'] = pd.Series(stock_price['Code'], dtype="string")
    stock_price['Code'] = stock_price['Code'].str.zfill(6)
    stock_price.set_index('Code', inplace=True)

    if stock_price['Date'].max() == start:
        return print("No Updates (stock_price_load_daily)")
    else:
        # 테이블 INSERT
        stock_price.to_sql('STOCK_PRICE', conn, if_exists='append')

    # commit 및 종료
    conn.commit()
    conn.close()

    return print("Job Success (stock_price_load_daily)")


index_load_daily()
stock_price_load_daily()

