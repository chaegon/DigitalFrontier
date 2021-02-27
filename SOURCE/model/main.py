from tensorflow.keras.models import *
from visualization import *
from datetime import datetime, timedelta

from tools import *
from usage import *

from os import path

# file_name = '316140'
col = ['Open', 'High', 'Low', 'Close','Volume']

dirpath = r'./'
if __name__ == '__main__':
    dirpath = r'../'
    '''
    run 학습 함수
    seq_len : 학습시킬 길이 or 테스트 데이터 셋 길이
    number  : 저장할 file name == 종목코드
    learning : True - 학습
               False - 예측
    
    '''

list_stock_code = []  # ['019990', '076610', '299900', '299910']

if len(list_stock_code) == 0:
    str_stock_code = input('Input Stock Code to Learning : ')
    if len(str_stock_code) != 6:
        print('Input Value is wrong. Stock code length must be 6. Re-run this.')
        exit(-1)
    else:
        list_stock_code.append(str_stock_code)

for stock_code in list_stock_code:
    str_data_file_path = dirpath + 'data/stock_price/' + stock_code + '.csv'
    if path.isfile(str_data_file_path) is not True:
        print('File not Exist ' + str_data_file_path)
        # TODO: create learning data file and continue process
        continue

    print('>>> target stock code ' + stock_code)
    print('>>> input file ' + str_data_file_path)

    print('>>> Learning')
    run(seq_len=30, number=stock_code, learning=True)

    print('>>> Prediction')
    run(seq_len=30, number=stock_code, learning=False)

    exit(0)