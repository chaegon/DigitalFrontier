from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from models import *
import copy

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from models import *


def read_data(path) :
    '''
    파일을 읽어 dataFrame으로 처리
    '''
    df = pd.read_csv(path)
    return df

def price_mean(data, col, Date = True) :
    avg = np.mean(data[col], axis=1)
    date = data.loc[:, 'Date'].values
    price = avg.values
    stock = pd.DataFrame()
    if Date :
        stock['Date'] = date
    stock['Price'] = price
    return stock


def preprocessing(df) :
    '''
    :param col_name: 특정한 컬럼만 Scale하고 싶을 경우 list로 컬럼 이름을 받는다.
    :param decoder:  MinMax Scaler를 다시 원복 시키고 싶을 때 (True, False)
    :return:

    MinMax Scaler를 통해 Nomarlization을 하거나 예측 후 주가를 원복 시키는데 사용한다.
    '''
    min_price = df['Price'].min()
    max_price = df['Price'].max()
    gap = max_price - min_price
    normal_price = (df['Price'] - min_price) / (max_price - min_price)
    normal = pd.DataFrame()
    normal['Date'] = df['Date']
    normal['Price'] = normal_price.values
    return normal, min_price, max_price, gap

def inverse_preprocessing(price, min_price, gap) :
    inverse_price = price * gap + min_price
    return inverse_price


def split_dataset(df, col) :
    '''
    train data, validation data, test data로 나누는 함수
    '''
    times = sorted(df.index.values)
    last_10pct = sorted(df.index.values)[-int(0.1 * len(times))]
    last_20pct = sorted(df.index.values)[-int(0.2 * len(times))]

    df_train = df[(df.index < last_20pct)]
    df_val = df[(df.index >= last_20pct) & (df.index < last_10pct)]
    df_test = df[(df.index >= last_10pct)]

    train_data = df_train[col].values
    val_data = df_val[col].values
    test_data = df_test[col].values
    # print('Training data shape: {}'.format(train_data.shape))
    # print('Validation data shape: {}'.format(val_data.shape))
    # print('Test data shape: {}'.format(test_data.shape))
    return df_train, train_data, df_val, val_data, df_test, test_data

def generate_label(data, seq_len) :
    x_data, y_data = [], []
    for i in range(seq_len, len(data)):
        x_data.append(data[i - seq_len:i])
        y_data.append(data[:, 3][i])
    x_data, y_data = np.array(x_data), np.array(y_data)

    assert x_data.shape[0] == y_data.shape[0] or x_data.shape[1] == y_data.shape[1]

    return x_data, y_data

def create_model(d_k, d_v, n_heads, ff_dim, seq_len):
  time_embedding = Time2Vector(seq_len)
  attn_layer1 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
  attn_layer2 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
  attn_layer3 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)


  in_seq = Input(shape=(seq_len,5))
  x = time_embedding(in_seq)
  x = Concatenate(axis=-1)([in_seq, x])
  x = attn_layer1((x, x, x))
  x = attn_layer2((x, x, x))
  x = attn_layer3((x, x, x))
  x = GlobalAveragePooling1D(data_format='channels_first')(x)
  x = Dropout(0.1)(x)
  x = Dense(64, activation='relu')(x)
  x = Dropout(0.1)(x)
  out = Dense(1, activation='linear')(x)

  model = Model(inputs=in_seq, outputs=out)
  model.compile(loss='mse', optimizer='adam', metrics=['mae', 'mape'])
  return model