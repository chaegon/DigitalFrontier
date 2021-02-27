from tensorflow.keras.models import *
from visualization import *
from datetime import datetime, timedelta

from tools import *
from usage import *

# file_name = '316140'
col = ['Open', 'High', 'Low', 'Close','Volume']

if __name__ == "__main__":
    '''
    run 학습 함수
    seq_len : 학습시킬 길이 or 테스트 데이터 셋 길이
    number  : 저장할 file name == 종목코드
    learning : True - 학습
               False - 예측
    
    '''

list_file_name = []

if len(list_file_name) == 0:
    str_stock_code = input('Input Stock Code to Learning : ')
    if len(str_stock_code) != 6:
        exit(0)
    else:
        list_file_name.append(str_stock_code)

for file_name in list_file_name:
    print('>>> Learning')
    run(seq_len=30, number=file_name, learning=True)

    print('>>> Prediction')
    run(seq_len=30, number=file_name, learning=False)
