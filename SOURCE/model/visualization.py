import matplotlib.pyplot as plt
import numpy as np


def visualization(df, save_path, x_col='Price', x_label='Price', y_col='Date', y_label='Avg Price', title='Price', name=None):
    try:
        fig = plt.figure(figsize=(15, 10))
        st = fig.suptitle("Price Flow", fontsize=20)
        st.set_y(0.92)
        ax1 = fig.add_subplot(211)
        ax1.plot(df[x_col], label='Price')
        ax1.set_xticks(range(0, df.shape[0], 5000))
        ax1.set_xticklabels(df[y_col].loc[::5000])
        ax1.set_ylabel(y_label, fontsize=18)
        # ax1.legend(loc="upper left", fontsize=12)
        plt.savefig(save_path)
    except:
        print('Graph of Stock Price is not saved ' + name)
        return 1
    return 0

def visualization_dataset(train_data, val_data, test_data, save_path, name = None) :
    try :
        fig = plt.figure(figsize=(15,12))
        st = fig.suptitle("Data Separation", fontsize=20)
        st.set_y(0.95)

        ax1 = fig.add_subplot(211)
        ax1.plot(np.arange(train_data.shape[0]), train_data['Price'], label='Training data')

        ax1.plot(np.arange(train_data.shape[0],
                           train_data.shape[0]+val_data.shape[0]), val_data['Price'], label='Validation data')

        ax1.plot(np.arange(train_data.shape[0]+val_data.shape[0],
                           train_data.shape[0]+val_data.shape[0]+test_data.shape[0]), test_data['Price'], label='Test data')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Normalization Price')
        ax1.set_title("Price", fontsize=18)
        ax1.legend(loc="best", fontsize=12)
        plt.savefig(save_path)
    except :
        print('Graph of Stock Price is not saved ' + name)
        return 1
    return 0