import sqlite3
import pandas as pd
import pandas_datareader.data as web
import datetime
import FinanceDataReader as fdr

# sqlite3 설치 필요
# sqlite3 설치 및 설정: https://somjang.tistory.com/entry/SQLite3-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0
# sqlite db browser 설치: https://sqlitebrowser.org/
# - 수행 시, 프로젝트 폴더에 DIGITALFRONTIER.db 파일 생성 및 테이블 생성

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

def index_load_daily():
    # 2. 추가적재
    #  - 마지막 적재 일로 부터 오늘날짜까지 적
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
        return
    else:
        # 테이블 INSERT
        kospi_df.to_sql('DAILY_KOSPI_INDEX', conn, if_exists='append')
        kosdaq_df.to_sql('DAILY_KOSDAQ_INDEX', conn, if_exists='append')
        kpi200_df.to_sql('DAILY_KPI200_INDEX', conn, if_exists='append')


def stocks_load_all():
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

    return

# 초기 적재 수행
#index_load_initial()

#일별 수행
#index_load_daily()

stocks_load_all()
