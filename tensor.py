'''
This script shows how to predict stock prices using a basic RNN
'''
import tensorflow as tf
import numpy as np
import matplotlib
import os
import pandas
import re

tf.set_random_seed(777)  # reproducibility

if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    matplotlib.use('Agg')

import matplotlib.pyplot as plt


def MinMaxScaler(data):
    ''' Min Max Normalization

    Parameters
    ----------
    data : numpy.ndarray
        input data to be normalized
        shape: [Batch size, dimension]

    Returns
    ----------
    data : numpy.ndarry
        normalized data
        shape: [Batch size, dimension]

    References
    ----------
    .. [1] http://sebastianraschka.com/Articles/2014_about_feature_scaling.html

    '''
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)

def DeMinMaxScaler(data):#수정 요
    return data*(np_max - np_min) + np_min

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub(' ', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', \
            '', cleaned_text)
    return cleaned_text


# train Parameters
timesteps = seq_length = 5 #학습시킬 데이터의 간격
data_dim = 2 # 학습시킬 데이터의 열의 갯수
hidden_dim = 10 
output_dim = 1
learing_rate = 0.01
iterations = 5630

# Open, High, Low, Volume, Close
xy = np.loadtxt('currency_log.txt', delimiter=',')
#xy2 = np.loadtxt('currency_log.txt', delimiter=',', usecols=1)
print("=======")
print(xy)
#xy = xy[0,1,2]
print("----------")
print(xy[:,[-2]])



#xy = xy[:,[-1]]  # reverse order (chronically ordered)
np_max = np.max(xy, 0)
np_min = np.min(xy, 0)
xy = MinMaxScaler(xy)
x = xy
y = xy[:,[-2]]  # Close as label

# build a dataset
dataX = []
dataY = []
for i in range(0, len(y) - seq_length):
    _x = x[i:i + seq_length]
    _y = y[i + seq_length]  # Next close price
    #print(_x, "->", _y)
    dataX.append(_x)
    dataY.append(_y)

# train/test split
train_size = int(len(dataY) * 0.9) # 90%
#train_size = int(len(dataY) - 1) # 70%
test_size = len(dataY) - train_size # 10%
trainX, testX = np.array(dataX[0:train_size]), np.array(
    dataX[train_size:len(dataX)])
trainY, testY = np.array(dataY[0:train_size]), np.array(
    dataY[train_size:len(dataY)])

# input place holders
X = tf.placeholder(tf.float32, [None, seq_length, data_dim])
Y = tf.placeholder(tf.float32, [None, 1])

# build a LSTM network
cell = tf.contrib.rnn.BasicLSTMCell(
    num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)

outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
Y_pred = tf.contrib.layers.fully_connected(
    outputs[:, -1], output_dim, activation_fn=None)  # We use the last cell's output

# cost/loss
loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
# optimizer
optimizer = tf.train.AdamOptimizer(learing_rate)
train = optimizer.minimize(loss)

# RMSE
targets = tf.placeholder(tf.float32, [None, 1])
predictions = tf.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    # Training step
    for i in range(iterations):
        _, step_loss = sess.run([train, loss], feed_dict={
                                X: trainX, Y: trainY})
        #print("[step: {}] loss: {}".format(i, step_loss))

    # Test step
    test_predict = sess.run(Y_pred, feed_dict={X: testX})
    rmse = sess.run(rmse, feed_dict={
                    targets: testY, predictions: test_predict})
    print("RMSE: {}".format(rmse))

    t_rmse = DeMinMaxScaler(rmse)
    print_testY = DeMinMaxScaler(testY)
    print_test_predict = DeMinMaxScaler(test_predict)
    #print_testY = (testY)
    #print_test_predict = (test_predict)
    
    # Plot predictions
    plt.plot(print_testY,label="Y")
    plt.plot(print_test_predict,label="Predict")
    
    plt.xlabel("Time Period")
    plt.ylabel("Dollar Price")
    pred_result = clean_text(str(print_test_predict[:,[-2]][-1]))
    print(pred_result)
    f = open("pred_usd_1.txt", 'w')
    f.write('{}\n'.format(pred_result))
    f.close()
    #print("----> ", print_testY)
    plt.show()
    plt.savefig('result.png')
