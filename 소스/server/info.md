# DigitalFrontier
DigitalFrontier

#1. 기본 환경 설정
- 파이썬 version: 3.8.5

- sqlite3 설치
  https://somjang.tistory.com/entry/SQLite3-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0 

- sqlite db browser
  https://sqlitebrowser.org/

#2. load_db.py 프로그램 설명

- index_load_initial()
  **** 최초 1회만 수행하면 됩니다.
  > 코스피, 코스닥, 코스피200 지수정보를 적재하는 기능으로 2014년 01월 01월 부터 수행날까지의 정보를 적재한다.
  > 적재 테이블: DAILY_KOSPI_INDEX, DAILY_KOSDAQ_INDEX, DAILY_KPI200_INDEX
  > 테이블 컬럼: Date, High, Low, Open, Close, Volume
  
  
- index_load_daily()
  > 코스피, 코스닥, 코스피200 지수정보를 적재하는 기능으로 index_load_initial()에 적재된 마지막 날짜이후부터 수행날 까지의 정보를 적재한다.
  > 적재 테이블: DAILY_KOSPI_INDEX, DAILY_KOSDAQ_INDEX, DAILY_KPI200_INDEX
  > 테이블 컬럼: Date, High, Low, Open, Close, Volume
  
  
- stock_load_all()
  **** 최초 1회만 수행하면 됩니다.
  **** kospi_data_20210124.csv 및 kosdaq_data_20210124.csv 파일 저장 필요합니다.
  > 코스피 및 코스닥 전체 종목코드 & 종목명을 적재한다.
  > 적재 테이블: CODE_DATA
  > 테이블 컬럼: Code, Name
  
- stock_price_load_initial()
  **** 최초 1회만 수행하시면 됩니다.
  > 전체 종목에 대한 일별 가격 정보를 2019년 01월 01일부터 수행날까지 적재한다.
  > 적재 테이블: STOCK_PRICE
  > 테이블 컬럼: Name, Code, Date, Open, High, Low, Close, Volume, Change
  
- stock_price_load_daily()
  > 전체 종목에 대한 일별 가격 정보를 2019년 01월 01일부터 수행날까지 적재한다.
  > 적재 테이블: STOCK_PRICE
  > 테이블 컬럼: Name, Code, Date, Open, High, Low, Close, Volume, Change
