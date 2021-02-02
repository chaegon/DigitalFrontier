from tensorflow.keras.models import *
from visualization import *
from tools import *


import matplotlib.pyplot as plt
plt.style.use('seaborn')

batch_size = 32
seq_len = 128

d_k = 256
d_v = 256
n_heads = 12
ff_dim = 256

data_path = r'./data/Stock_Price.csv'
save_path = r'./freezing/'
file_name = 'AIStock.hdf5'

structure_origin = r'./images/structure_origin.png'
structure_normal = r'./images/structure_normal.png'
structure_dataset = r'./images/structure_dataset.png'
structure_pred = r'./images/structure_pred.png'
structure_model = r'./images/structure_model.png'



col = ['Open', 'High', 'Low', 'Close','Volume']

if __name__ == "__main__" :

    # '''
    # gpu 확인
    # '''
    # gpus = tf.config.experimental.list_physical_devices('GPU')
    # if gpus:
    #     # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
    #     try:
    #         tf.config.experimental.set_virtual_device_configuration(
    #             gpus[0],
    #             [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
    #     except RuntimeError as e:
    #         # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
    #         print(e)
    #
    # '''
    # 전처리 및 데이터 split
    # '''
    data = read_data(data_path)
    # #print(data)
    # stock = price_mean(data, col)
    #
    # visualization(stock, save_path= structure_origin, name='Preprocessing')
    # normal, max_num, min_num, gap = preprocessing(stock)
    # #normal.head()
    # visualization(normal, save_path= structure_normal, y_label='Normal Price', name='normal')
    #
    df_train, train_data, df_val, val_data, df_test, test_data = split_dataset(data, col)
    # train_stock = price_mean(df_train, col, False)
    # vali_stock = price_mean(df_val, col, False)
    # test_stock = price_mean(df_test, col, False)
    #
    # # print(train_stock)
    #
    # visualization_dataset(train_stock,vali_stock, test_stock, save_path= structure_dataset, name = 'splite')
    #
    x_train, y_train = generate_label(train_data, seq_len)
    x_val, y_val = generate_label(val_data, seq_len)
    x_test, y_test = generate_label(test_data, seq_len)
    #
    # # print('Training set shape', x_train.shape, y_train.shape)
    # # print('Validation set shape', x_val.shape, y_val.shape)
    # # print('Testing set shape', x_test.shape, y_test.shape)
    #
    #
    # '''
    # gpu 셋팅
    # '''
    # tf.config.set_soft_device_placement(True)
    # tf.debugging.set_log_device_placement(True)
    #
    # '''
    # 모델 생성
    # '''
    # model = create_model(d_k,d_v,n_heads, ff_dim, seq_len)
    # model.summary()
    #
    # callback = tf.keras.callbacks.ModelCheckpoint(save_path+file_name,
    #                                               monitor='val_loss',
    #                                               save_best_only=True, verbose=1)
    #
    # history = model.fit(x_train, y_train,
    #                     batch_size=batch_size,
    #                     epochs=1,
    #                     callbacks=[callback],
    #                     validation_data=(x_val, y_val))

    model = tf.keras.models.load_model(save_path+file_name,
                                       custom_objects={'Time2Vector': Time2Vector,
                                                       'SingleAttention': SingleAttention,
                                                       'MultiAttention': MultiAttention,
                                                       'TransformerEncoder': TransformerEncoder})

    train_pred = model.predict(x_train)
    val_pred = model.predict(x_val)
    test_pred = model.predict(x_test)

    train_eval = model.evaluate(x_train, y_train, verbose=0)
    val_eval = model.evaluate(x_val, y_val, verbose=0)
    test_eval = model.evaluate(x_test, y_test, verbose=0)
    print(' ')
    print('Training Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(train_eval[0], train_eval[1], train_eval[2]))
    print('Validation Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(val_eval[0], val_eval[1], val_eval[2]))
    print('Test Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(test_eval[0], test_eval[1], test_eval[2]))

    tf.keras.utils.plot_model(
        model,
        to_file= structure_model,
        show_shapes=True,
        show_layer_names=True,
        expand_nested=True,
        dpi=96, )

    visualization_dataset(train_pred, val_pred, test_pred, save_path=structure_pred, name='splite')



