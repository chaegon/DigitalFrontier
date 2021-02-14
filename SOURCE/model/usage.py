from tensorflow.keras.models import *
from visualization import *
from datetime import datetime, timedelta

from tools import *


import matplotlib.pyplot as plt

# 076610

def run(seq_len = 1, number =  'AIStock', learning = True) :
    batch_size = 1

    d_k = 256
    d_v = 256
    n_heads = 12
    ff_dim = 256

    data_path = r'../data/' + number + '.csv'
    pred_path = r'../data/' + number + '_pred.csv'
    normal_path = r'../data/' + number + '_normal.csv'

    save_path = r'../freezing/' + number + '.hdf5'

    structure_origin = r'../images/' + number + '_origin.png'
    structure_dataset = r'../images/' + number + '_dataset.png'
    structure_pred = r'../images/' + number + '_pred.png'
    structure_model = r'../images/' + number + '_model.png'
    col = ['Open', 'High', 'Low', 'Close', 'Volume']

    data = read_data(data_path)
    '''
    Normalization
    '''
    normal = pd.DataFrame()
    normal['Date'] = data['Date']

    price_min = 0
    price_max = 0
    price_gap = 0

    for i in col:
        price, min_price, max_price, gap = preprocessing(data, i)
        normal[i] = price[i].values
        price_min += min_price
        price_max += max_price
        price_gap += gap

    price_min = price_min / 5
    price_max = price_max / 5
    price_gap = price_gap / 5


    df_train, train_data, df_val, val_data, df_test, test_data = split_dataset(normal, col)

    x_train, y_train = generate_label(train_data, seq_len)
    x_val, y_val = generate_label(val_data, seq_len)
    x_test, y_test = generate_label(test_data, seq_len)

    # print('Training set shape', x_train.shape, y_train.shape)
    # print('Validation set shape', x_val.shape, y_val.shape)
    # print('Testing set shape', x_test.shape, y_test.shape)

    test_set = generate_pred_data(normal[col], seq_len)
    print(test_set.shape)
    if learning :
        normal.to_csv(normal_path)
        #
        # '''
        # 전처리 및 데이터 split
        # '''
        stock = price_mean(data, col)

        visualization(stock, save_path= structure_origin, name='Preprocessing')
        # normal, max_num, min_num, gap = preprocessing(stock)
        #normal.head()
        # visualization(normal, save_path= structure_normal, y_label='Normal Price', name='normal')
        #

        train_stock = price_mean(df_train, col, False)
        vali_stock = price_mean(df_val, col, False)
        test_stock = price_mean(df_test, col, False)

        # print(train_stock)

        # visualization_dataset(train_stock,vali_stock, test_stock, save_path= structure_dataset, name = 'splite')


        # print('Training set shape', x_train.shape, y_train.shape)
        # print('Validation set shape', x_val.shape, y_val.shape)
        # print('Testing set shape', x_test.shape, y_test.shape)


        '''
        gpu 셋팅
        '''
        tf.config.set_soft_device_placement(True)
        # tf.debugging.set_log_device_placement(True)

        '''
        모델 생성
        '''
        model = create_model(d_k,d_v,n_heads, ff_dim, seq_len)
        model.summary()

        callback = tf.keras.callbacks.ModelCheckpoint(save_path,
                                                      monitor='val_loss',
                                                      save_best_only=True, verbose=1)

        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=35,
                            callbacks=[callback],
                            validation_data=(x_val, y_val))
    else :

        model = tf.keras.models.load_model(save_path,
                                           custom_objects={'Time2Vector': Time2Vector,
                                                           'SingleAttention': SingleAttention,
                                                           'MultiAttention': MultiAttention,
                                                           'TransformerEncoder': TransformerEncoder})



        print('It starts to predict ', test_set.shape)
        test_pred = model.predict(test_set)
        print('It finishes predicting shape -> ', test_pred.shape)

        tf.keras.utils.plot_model(
            model,
            to_file=structure_model,
            show_shapes=True,
            show_layer_names=True,
            expand_nested=True,
            dpi=96, )
        df_pred_test = pd.DataFrame()
        df_pred_test['Date'] = pd.DatetimeIndex(normal['Date'][-seq_len:]) + timedelta(days=seq_len)
        df_pred_test['Price'] = inverse_preprocessing(test_pred, gap = int(price_gap), min_price=int(price_min))


        df_pred_test.to_csv(pred_path)
        print('prediction is saved successfully')
        # visualization(df_pred_test, save_path=structure_pred, y_label='Prediction Price', name='Predict')

